# 2NF table checks

Checked by `scripts/verify_2nf.py` against both `1NF/construction_1nf.csv` and the raw file.

## Duplicates and primary keys

| File | Primary key | Rows | Duplicate rows | Duplicate keys | Values match raw |
|---|---|---|---|---|---|
| projects.csv | ProjectID | 7 | 0 | 0 | yes |
| workers.csv | WorkerID | 5 | 0 | 0 | yes |
| suppliers.csv | SupplierID | 6 | 0 | 0 | yes |
| project_material_supply.csv | (ProjectID, SupplierID, MaterialSupplied) | 16 | 0 | 0 | yes |
| project_equipment.csv | (ProjectID, EquipmentUsed) | 13 | 0 | 0 | yes |
| project_resource_links.csv | all 8 columns | 280 | 0 | 0 | (checked by the join below) |

The row counts are the same as the ones in the document's Stage 2 table.

ProjectName, WorkerName and SupplierName are each unique, so every surrogate key (W01–W05, S01–S06)
stands for exactly one name.

## Spot checks by hand

- **projects.csv, P004:** Green Tech Campus, Commercial, 2024-04-01 to 2025-02-28, 900 Innovation Way,
  New York, NY, FutureTech Ltd, John Carter. Same as raw rows 8 and 9.
- **workers.csv, W01:** Mike Ross, 617-555-3001, 45. He appears on 4 raw rows (P001, P002, P004, P006),
  always with the same phone and rate, and is stored once.
- **suppliers.csv, S02:** SteelWorks Inc, Chicago. Raw rows 3, 8 and 14 are now one row.
- **project_material_supply.csv:** P001/S01 has Concrete 120 and Steel 300, the raw pairing.
  P004 has Glass Panels twice, from S02 (SteelWorks) and S04 (Global Glass). This is correct, because
  SupplierID is part of the key.
- **project_equipment.csv:** Crane is 5000 on P001, 5500 on P002, 6000 on P004 and 6500 on P007.
  Each cost is kept with its own project.

## Dependencies

All five partial dependencies listed in the document hold on every 1NF row:

| Part of the key | Depends on it |
|---|---|
| ProjectID | 13 project, site, client and supervisor columns |
| WorkerName | WorkerPhone, WorkerHourlyRate |
| SupplierName | SupplierCity |
| (ProjectID, SupplierName, MaterialSupplied) | MaterialUnitCost |
| (ProjectID, EquipmentUsed) | EquipmentRentalCost |

For the two tables with composite keys, each smaller part of the key was tested:

- **project_equipment:** neither ProjectID nor EquipmentUsed alone determines the cost, so the
  cost needs the whole key.
- **project_material_supply:** five of the six smaller combinations fail, but
  (ProjectID, MaterialSupplied) happens to determine the cost in this sample. See
  [findings_and_corrections.md](findings_and_corrections.md), finding 2.

## Foreign keys and lossless join

- Every ProjectID, WorkerID and SupplierID in project_resource_links, project_material_supply and
  project_equipment exists in its parent table (0 orphans).
- Every link row has a matching price in project_material_supply and a matching cost in project_equipment.
- Joining all 6 tables back together rebuilds the 1NF file exactly: 280 rows, no rows missing and no extra rows.
  The 2NF split lost no information and added none.
