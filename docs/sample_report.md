# CMDB Health Report

Generated: 2026-09-24 17:18 UTC  
CIs evaluated: **53**

| KPI | Score |
|---|---|
| Completeness | 75.5% |
| Correctness | 45.3% |
| Compliance | 66.0% |

## Findings by rule

| Rule | Count |
|---|---|
| duplicate_name | 4 |
| duplicate_serial | 6 |
| missing_required_fields | 13 |
| never_discovered | 1 |
| orphan_ci | 27 |
| stale_ci | 17 |

## Remediation queue

| CI | KPI | Rule | Detail |
|---|---|---|---|
| demo-srv-002 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-002 | compliance | stale_ci | Last discovered 113 days ago |
| demo-srv-003 | completeness | missing_required_fields | owned_by |
| demo-srv-004 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-004 | compliance | stale_ci | Last discovered 68 days ago |
| demo-srv-006 | completeness | missing_required_fields | owned_by |
| demo-srv-006 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-007 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-008 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-009 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-010 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-011 | completeness | missing_required_fields | owned_by |
| demo-srv-011 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-012 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-013 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-015 | completeness | missing_required_fields | owned_by |
| demo-srv-017 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-017 | compliance | stale_ci | Last discovered 68 days ago |
| demo-srv-019 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-020 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-021 | completeness | missing_required_fields | owned_by |
| demo-srv-021 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-022 | compliance | stale_ci | Last discovered 113 days ago |
| demo-srv-023 | completeness | missing_required_fields | owned_by |
| demo-srv-024 | compliance | stale_ci | Last discovered 113 days ago |
| demo-srv-025 | completeness | missing_required_fields | owned_by |
| demo-srv-025 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-026 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-026 | compliance | stale_ci | Last discovered 68 days ago |
| demo-srv-028 | compliance | stale_ci | Last discovered 68 days ago |
| demo-srv-029 | completeness | missing_required_fields | owned_by |
| demo-srv-029 | compliance | stale_ci | Last discovered 68 days ago |
| demo-srv-030 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-032 | completeness | missing_required_fields | owned_by |
| demo-srv-033 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-034 | compliance | stale_ci | Last discovered 68 days ago |
| demo-srv-035 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-036 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-037 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-039 | completeness | missing_required_fields | owned_by |
| demo-srv-039 | compliance | stale_ci | Last discovered 68 days ago |
| demo-srv-040 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-040 | compliance | stale_ci | Last discovered 68 days ago |
| DEMO-SRV-001 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-002-old | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-002-old | compliance | stale_ci | Last discovered 113 days ago |
| demo-srv-003 | completeness | missing_required_fields | owned_by |
| demo-srv-003 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-003 | compliance | never_discovered | last_discovered is empty |
| Demo App 1 | compliance | stale_ci | Last discovered 63 days ago |
| Demo App 2 | compliance | stale_ci | Last discovered 30 days ago |
| Demo App 3 | completeness | missing_required_fields | owned_by |
| Demo App 4 | compliance | stale_ci | Last discovered 63 days ago |
| Demo App 7 | compliance | stale_ci | Last discovered 63 days ago |
| Demo App 9 | completeness | missing_required_fields | owned_by |
| Demo App 9 | correctness | orphan_ci | No upstream or downstream relationships |
| Demo App 9 | compliance | stale_ci | Last discovered 63 days ago |
| Demo App 10 | correctness | orphan_ci | No upstream or downstream relationships |
| demo-srv-001 | correctness | duplicate_serial | Shares 'SN-DEMO-00001' with: srv0001, srv9001 |
| DEMO-SRV-001 | correctness | duplicate_serial | Shares 'SN-DEMO-00001' with: srv0001, srv9001 |
| demo-srv-002 | correctness | duplicate_serial | Shares 'SN-DEMO-00002' with: srv0002, srv9002 |
| demo-srv-002-old | correctness | duplicate_serial | Shares 'SN-DEMO-00002' with: srv0002, srv9002 |
| demo-srv-003 | correctness | duplicate_serial | Shares 'SN-DEMO-00003' with: srv0003, srv9003 |
| demo-srv-003 | correctness | duplicate_serial | Shares 'SN-DEMO-00003' with: srv0003, srv9003 |
| demo-srv-001 | correctness | duplicate_name | Shares 'demo-srv-001' with: srv0001, srv9001 |
| DEMO-SRV-001 | correctness | duplicate_name | Shares 'demo-srv-001' with: srv0001, srv9001 |
| demo-srv-003 | correctness | duplicate_name | Shares 'demo-srv-003' with: srv0003, srv9003 |
| demo-srv-003 | correctness | duplicate_name | Shares 'demo-srv-003' with: srv0003, srv9003 |
