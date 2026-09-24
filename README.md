[README.md](https://github.com/user-attachments/files/32628526/README.md)
# ServiceNow CMDB Health Analyzer

Offline scoring of CMDB **completeness, correctness, and compliance** — the same three KPIs ServiceNow's CMDB Health Dashboard reports — against an exported set of CIs and relationships.

> **Portfolio project.** This is an independently written, clean-room demonstration built with synthetic data. It is not code from, or a copy of, any employer's or client's ServiceNow instance.

## Business problem

Incident and change teams depend on the CMDB for impact analysis. When CIs are duplicated, missing owners, orphaned from services, or no longer seen by Discovery, the impact data they get is wrong. Platform teams need a repeatable way to measure CMDB quality and to generate a prioritized remediation queue for CI owners, including outside the instance (pre-migration checks, CI pipelines, audits).

## What it checks

| KPI | Rule | ServiceNow concept |
|---|---|---|
| Completeness | `missing_required_fields`: class-specific mandatory attributes (owner, support group, serial, IP, OS) | CMDB Health completeness / recommended fields |
| Correctness | `duplicate_serial`, `duplicate_name`: same class + identifier | Identification & Reconciliation Engine (IRE) duplicate CIs |
| Correctness | `orphan_ci`: servers, apps and DB instances with no relationships | Orphan CI rules |
| Compliance | `stale_ci`, `never_discovered`: `last_discovered` older than N days or empty | Staleness rules |

Retired CIs (`install_status = 7`) are excluded.

## Architecture

```
 Table API / CSV export              cmdb_health.analyzer               Output
┌──────────────────────┐   load    ┌───────────────────────┐   render   ┌────────────────────┐
│ cmdb_ci_* records     │ ───────▶ │ completeness rules     │ ─────────▶ │ Markdown report     │
│ cmdb_rel_ci records   │          │ duplicate / orphan     │            │ JSON (for PA / BI)  │
└──────────────────────┘          │ staleness rules        │            │ exit code (CI gate) │
                                   └───────────────────────┘            └────────────────────┘
```

## Quick start

```bash
pip install -e ".[dev]"
python scripts/generate_sample_data.py          # synthetic data with seeded issues
cmdb-health --cis data/cis.json --rels data/rels.json --out docs/sample_report.md
pytest -q
```

Input can be a raw Table API payload (`{"result": [...]}`), a JSON list, or a CSV export. To pull live data, use the companion repo `servicenow-table-api-toolkit` against a **personal developer instance (PDI)**, never a production instance you are not authorized to export.

### Options

| Flag | Default | Purpose |
|---|---|---|
| `--stale-days` | 30 | Days since `last_discovered` before a CI is stale |
| `--format` | markdown | `markdown` or `json` |
| `--min-score` | 0 | Exit code 1 if any KPI falls below this (pipeline quality gate) |

### Docker

```bash
docker build -t cmdb-health .
docker run --rm -v "$PWD/data:/data" cmdb-health --cis /data/cis.json --rels /data/rels.json
```

## Sample output

From the synthetic dataset (53 CIs), see [`docs/sample_report.md`](docs/sample_report.md):

| KPI | Score |
|---|---|
| Completeness | 75.5% |
| Correctness | 45.3% |
| Compliance | 66.0% |

## Security considerations

- Contains no credentials and never connects to an instance by itself.
- Sample data uses RFC 5737 documentation IP ranges and fake serials and names.
- CMDB exports can contain sensitive infrastructure detail. Keep real exports out of version control (`.gitignore` excludes `reports/` and `*.local.json`).

## Limitations and next steps

- Duplicate detection uses exact class + serial/name matches. IRE also uses weighted identifier entries and independent/dependent rules.
- Relationship checks don't validate CSDM layer correctness (for example, an application service without an owning business service).
- Planned: CSDM layer validation, a configurable rules file (YAML), and a Performance Analytics-compatible JSON output.

## License

MIT
