from datetime import datetime, timezone

import pytest

from cmdb_health import analyze
from cmdb_health.cli import main

NOW = datetime(2026, 9, 1, tzinfo=timezone.utc)


def server(sys_id, **kw):
    base = {"sys_id": sys_id, "name": sys_id, "sys_class_name": "cmdb_ci_linux_server",
            "serial_number": f"SN-{sys_id}", "ip_address": "192.0.2.1", "os": "Linux",
            "owned_by": "owner.alpha", "support_group": "Linux Ops",
            "last_discovered": "2026-08-31 00:00:00", "install_status": "1"}
    base.update(kw)
    return base


def rules(report):
    return {(f.ci_sys_id, f.rule) for f in report.findings}


def test_healthy_ci_scores_100():
    report = analyze([server("a")], [{"parent": "x", "child": "a"}], now=NOW)
    assert report.findings == []
    assert report.summary()["completeness"] == 100.0


def test_missing_owner_is_completeness_finding():
    report = analyze([server("a", owned_by="")], [{"parent": "x", "child": "a"}], now=NOW)
    assert ("a", "missing_required_fields") in rules(report)
    assert report.score("completeness") == 0.0


def test_duplicate_serial_is_case_insensitive():
    cis = [server("a", serial_number="abc1"), server("b", serial_number="ABC1")]
    report = analyze(cis, [{"parent": "a", "child": "b"}], now=NOW)
    assert {("a", "duplicate_serial"), ("b", "duplicate_serial")} <= rules(report)


def test_orphan_and_stale_detection():
    report = analyze([server("a", last_discovered="2026-06-01 00:00:00")], [], now=NOW)
    assert ("a", "orphan_ci") in rules(report)
    assert ("a", "stale_ci") in rules(report)


def test_never_discovered_and_bad_timestamp():
    report = analyze([server("a", last_discovered=""), server("b", last_discovered="not-a-date")],
                     [{"parent": "a", "child": "b"}], now=NOW)
    assert ("a", "never_discovered") in rules(report)
    assert ("b", "never_discovered") in rules(report)


def test_retired_cis_are_excluded():
    report = analyze([server("a", install_status="7")], [], now=NOW)
    assert report.total_cis == 0


def test_cli_missing_file_returns_2(tmp_path):
    assert main(["--cis", str(tmp_path / "nope.json"), "--rels", str(tmp_path / "nope.json")]) == 2


def test_cli_min_score_gate(tmp_path):
    import json
    cis = tmp_path / "cis.json"
    rels = tmp_path / "rels.json"
    cis.write_text(json.dumps({"result": [server("a", owned_by="")]}))
    rels.write_text(json.dumps([]))
    out = tmp_path / "r.md"
    assert main(["--cis", str(cis), "--rels", str(rels), "--min-score", "90", "--out", str(out)]) == 1
    assert "CMDB Health Report" in out.read_text()


@pytest.mark.parametrize("fmt", ["json", "markdown"])
def test_cli_formats(tmp_path, capsys, fmt):
    import json
    cis = tmp_path / "cis.json"
    cis.write_text(json.dumps([server("a")]))
    rels = tmp_path / "rels.json"
    rels.write_text(json.dumps([{"parent": "x", "child": "a"}]))
    assert main(["--cis", str(cis), "--rels", str(rels), "--format", fmt]) == 0
    assert capsys.readouterr().out
