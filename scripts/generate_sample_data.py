"""Generate a synthetic CMDB export with deliberately seeded data-quality issues.

No real hostnames, IPs, serial numbers, or people are used. IPs come from the
RFC 5737 documentation ranges (192.0.2.0/24, 198.51.100.0/24).
"""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
OUT = Path(__file__).resolve().parent.parent / "data"
NOW = datetime(2026, 9, 1)
GROUPS = ["Linux Ops", "Windows Ops", "Network Eng", "App Support - Payments", "DBA Team"]
OWNERS = ["owner.alpha", "owner.bravo", "owner.charlie", ""]


def ts(days_ago: int) -> str:
    return (NOW - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    cis, rels = [], []
    for i in range(1, 41):
        cls = random.choice(["cmdb_ci_linux_server", "cmdb_ci_win_server"])
        cis.append({
            "sys_id": f"srv{i:04d}", "name": f"demo-srv-{i:03d}", "sys_class_name": cls,
            "serial_number": f"SN-DEMO-{i:05d}", "ip_address": f"192.0.2.{i}",
            "os": "Linux" if "linux" in cls else "Windows",
            "owned_by": random.choice(OWNERS), "support_group": random.choice(GROUPS),
            "last_discovered": ts(random.choice([1, 2, 3, 5, 45, 90])), "install_status": "1",
        })
    # Seed duplicates and a never-discovered CI.
    cis.append({**cis[0], "sys_id": "srv9001", "name": "DEMO-SRV-001"})
    cis.append({**cis[1], "sys_id": "srv9002", "name": "demo-srv-002-old"})
    cis.append({**cis[2], "sys_id": "srv9003", "last_discovered": ""})
    for i in range(1, 11):
        cis.append({"sys_id": f"app{i:04d}", "name": f"Demo App {i}", "sys_class_name": "cmdb_ci_appl",
                    "owned_by": random.choice(OWNERS), "support_group": random.choice(GROUPS),
                    "last_discovered": ts(random.choice([1, 7, 40])), "install_status": "1"})
        for s in random.sample(range(1, 41), 3):
            if i <= 8:  # apps 9 and 10 stay orphaned on purpose
                rels.append({"parent": f"app{i:04d}", "child": f"srv{s:04d}", "type": "Runs on::Runs"})
    OUT.mkdir(exist_ok=True)
    (OUT / "cis.json").write_text(json.dumps({"result": cis}, indent=2))
    (OUT / "rels.json").write_text(json.dumps({"result": rels}, indent=2))
    print(f"Wrote {len(cis)} CIs and {len(rels)} relationships to {OUT}")


if __name__ == "__main__":
    main()
