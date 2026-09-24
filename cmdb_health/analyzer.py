"""CMDB health scoring modeled on ServiceNow's completeness / correctness / compliance KPIs.

Works on an exported list of configuration items (CIs) plus relationships, so it can
run offline against a CSV/JSON export or against records pulled via the Table API.
All sample data in this repository is synthetic.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Iterable

log = logging.getLogger(__name__)

# Fields each CI class is expected to have populated (completeness rule).
DEFAULT_REQUIRED_FIELDS: dict[str, list[str]] = {
    "cmdb_ci_server": ["name", "serial_number", "ip_address", "os", "owned_by", "support_group"],
    "cmdb_ci_linux_server": ["name", "serial_number", "ip_address", "os", "owned_by", "support_group"],
    "cmdb_ci_win_server": ["name", "serial_number", "ip_address", "os", "owned_by", "support_group"],
    "cmdb_ci_netgear": ["name", "serial_number", "ip_address", "support_group"],
    "cmdb_ci_appl": ["name", "owned_by", "support_group"],
    "cmdb_ci_db_instance": ["name", "owned_by", "support_group"],
    # Note: "busines_criticality" is the platform's actual (misspelled) field name.
    "cmdb_ci_service_business": ["name", "owned_by", "busines_criticality"],
}

# Classes that must be related to something to be useful for impact analysis.
RELATIONSHIP_REQUIRED = {"cmdb_ci_appl", "cmdb_ci_db_instance", "cmdb_ci_server",
                         "cmdb_ci_linux_server", "cmdb_ci_win_server"}


@dataclass
class Finding:
    ci_sys_id: str
    ci_name: str
    kpi: str          # completeness | correctness | compliance
    rule: str
    detail: str


@dataclass
class HealthReport:
    total_cis: int
    findings: list[Finding] = field(default_factory=list)

    def _failed(self, kpi: str) -> set[str]:
        return {f.ci_sys_id for f in self.findings if f.kpi == kpi}

    def score(self, kpi: str) -> float:
        """Percentage of CIs with no findings for the KPI (0-100)."""
        if self.total_cis == 0:
            return 100.0
        return round(100.0 * (self.total_cis - len(self._failed(kpi))) / self.total_cis, 1)

    def summary(self) -> dict:
        by_rule: dict[str, int] = defaultdict(int)
        for f in self.findings:
            by_rule[f.rule] += 1
        return {
            "total_cis": self.total_cis,
            "completeness": self.score("completeness"),
            "correctness": self.score("correctness"),
            "compliance": self.score("compliance"),
            "findings_by_rule": dict(sorted(by_rule.items())),
        }


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    log.warning("Unparseable timestamp %r; treating as missing", value)
    return None


def analyze(
    cis: Iterable[dict],
    relationships: Iterable[dict],
    *,
    now: datetime | None = None,
    stale_after_days: int = 30,
    required_fields: dict[str, list[str]] | None = None,
) -> HealthReport:
    """Run completeness, correctness (duplicates, orphans) and compliance (staleness) rules."""
    now = now or datetime.now(timezone.utc)
    required_fields = required_fields or DEFAULT_REQUIRED_FIELDS
    cis = [c for c in cis if c.get("install_status", "1") not in {"7", "retired"}]
    report = HealthReport(total_cis=len(cis))

    related: set[str] = set()
    for rel in relationships:
        related.add(rel.get("parent", ""))
        related.add(rel.get("child", ""))

    serial_index: dict[tuple[str, str], list[dict]] = defaultdict(list)
    name_index: dict[tuple[str, str], list[dict]] = defaultdict(list)

    for ci in cis:
        sys_id, name, cls = ci.get("sys_id", ""), ci.get("name", ""), ci.get("sys_class_name", "")
        if not sys_id:
            log.error("CI without sys_id skipped: %r", ci)
            continue

        # Completeness
        missing = [f for f in required_fields.get(cls, ["name"]) if not str(ci.get(f, "")).strip()]
        if missing:
            report.findings.append(Finding(sys_id, name, "completeness", "missing_required_fields",
                                           ", ".join(missing)))

        # Correctness: orphan CIs
        if cls in RELATIONSHIP_REQUIRED and sys_id not in related:
            report.findings.append(Finding(sys_id, name, "correctness", "orphan_ci",
                                           "No upstream or downstream relationships"))

        serial = str(ci.get("serial_number", "")).strip().upper()
        if serial:
            serial_index[(cls, serial)].append(ci)
        if name:
            name_index[(cls, name.strip().lower())].append(ci)

        # Compliance: stale (not seen by Discovery / integrations)
        last_seen = _parse_ts(ci.get("last_discovered"))
        if last_seen is None:
            report.findings.append(Finding(sys_id, name, "compliance", "never_discovered",
                                           "last_discovered is empty"))
        elif now - last_seen > timedelta(days=stale_after_days):
            report.findings.append(Finding(sys_id, name, "compliance", "stale_ci",
                                           f"Last discovered {(now - last_seen).days} days ago"))

    # Correctness: duplicates (same class + serial, or same class + name)
    flagged: set[tuple[str, str]] = set()
    for rule, index in (("duplicate_serial", serial_index), ("duplicate_name", name_index)):
        for key, group in index.items():
            if len(group) < 2:
                continue
            ids = ", ".join(sorted(c["sys_id"] for c in group))
            for ci in group:
                if (ci["sys_id"], rule) in flagged:
                    continue
                flagged.add((ci["sys_id"], rule))
                report.findings.append(Finding(ci["sys_id"], ci.get("name", ""), "correctness", rule,
                                               f"Shares {key[1]!r} with: {ids}"))
    return report
