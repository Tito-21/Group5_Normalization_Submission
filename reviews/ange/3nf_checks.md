# 3NF checks

Checked by `scripts/verify_3nf_bcnf.py` against `2NF/projects.csv` and the 3NF folder.

## The transitive dependencies are real

| Dependency | Holds in 2NF/projects? | Why it is transitive |
|---|---|---|
| ClientName -> ClientPhone, ClientEmail, ClientCity | Yes | ClientName is not a key: Metro Corp, City Transit Auth and Retail Ventures each appear twice |
| SupervisorName -> SupervisorPhone | Yes | SupervisorName is not a key: John Carter (2), Sarah Lee (3), David Kim (2) |

## Lossless join

`projects JOIN clients ON ClientID JOIN supervisors ON SupervisorID` gives exactly the 7 rows of
`2NF/projects.csv`. No null foreign keys, no orphans, no missing or extra rows.

## Tables

| File | Primary key | Rows | Duplicate rows | Duplicate keys |
|---|---|---|---|---|
| projects.csv | ProjectID | 7 | 0 | 0 |
| clients.csv | ClientID | 4 | 0 | 0 |
| supervisors.csv | SupervisorID | 3 | 0 | 0 |
| workers, suppliers, project_material_supply, project_equipment, project_resource_links | unchanged | 5, 6, 16, 13, 280 | 0 | 0 |

The five unchanged tables are byte-for-byte equal to their 2NF versions.
ClientName and ClientEmail are unique in clients.csv, so they are valid alternate keys.

## Hand check

- P001 and P005 both use C01 (Metro Corp). Its phone 617-555-1000 is now stored once.
- P002 and P007 both use C02 and SV02. Sarah Lee's phone 617-555-2100 is stored once in supervisors.csv.

**Result: Stage 3 is correct.**
