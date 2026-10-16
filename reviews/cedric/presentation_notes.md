# Presentation notes: Stage 1 (1NF) and Stage 2 (2NF)

About 4 minutes. Show `1NF/construction_1nf.csv` and the `2NF/` folder on screen.

---

## Stage 1: First Normal Form

**The rule.** A table is in 1NF when every cell holds one value, there are no repeating groups,
and every row can be identified.

**What was wrong.** Seven raw columns held lists separated by `|`. Raw row 1 shows all of them:

```
WorkerSkills          Carpentry|Framing
WorkerCertifications  OSHA|First Aid
SupplierPhones        617-555-9000|617-555-9001
MaterialSupplied      Concrete|Steel        MaterialUnitCost     120|300
EquipmentUsed         Crane|Bulldozer       EquipmentRentalCost  5000|3000
```

**What we did.**

1. Split every list on `|` and renamed the columns to singular: WorkerSkill, WorkerCertification, SupplierPhone.
2. Split material and cost **together**, by position: 1st material with 1st cost. If they were split
   separately we would invent "Concrete costs 300", which is false. The same goes for equipment.
3. Replaced each raw row with one row per combination. Row 1 gives 2 × 2 × 2 × 2 × 2 = 32 rows.

**New rows, not new tables.** We kept one table on purpose. This stage only shows that the values are atomic.
The table grows from 15 to 280 rows, and that redundancy (Downtown Plaza is repeated 72 times) is the
reason for the next stages.

**The key.** (ProjectID, WorkerName, WorkerSkill, WorkerCertification, SupplierName, SupplierPhone,
MaterialSupplied, EquipmentUsed). We picked it from what a row means, not from what is unique in the sample.
In the sample, 5 columns happen to be unique, but a second carpenter on P001 would break that.

**How I checked it.** I traced rows 1, 9 and 15 by hand (32, 4 and 4 rows) and checked all 15 rows with
`scripts/verify_1nf.py`. Every value is there, every cost stays with its own material, and the total is 280.

---

## Stage 2: Second Normal Form

**The rule.** In 1NF, and no non-key column depends on only *part* of a composite key.

**The problem.** The 1NF key has 8 columns, but no non-key column needs all 8:

| Part of the key | Depends only on that part |
|---|---|
| ProjectID | project name, type, dates, site, client, supervisor |
| WorkerName | WorkerPhone, WorkerHourlyRate |
| SupplierName | SupplierCity |
| (ProjectID, SupplierName, MaterialSupplied) | MaterialUnitCost |
| (ProjectID, EquipmentUsed) | EquipmentRentalCost |

Example: Mike Ross's phone and rate are repeated on all 84 of his 1NF rows. If his rate changes,
84 rows must change.

**What we did.** Each group of columns moved to its own table, keyed by the part it depends on:

| File | Primary key | Rows |
|---|---|---|
| projects.csv | ProjectID | 7 |
| workers.csv | WorkerID | 5 |
| suppliers.csv | SupplierID | 6 |
| project_material_supply.csv | (ProjectID, SupplierID, MaterialSupplied) | 16 |
| project_equipment.csv | (ProjectID, EquipmentUsed) | 13 |
| project_resource_links.csv | all 8 key columns | 280 |

**Keys.** New surrogate keys WorkerID (W01–W05) and SupplierID (S01–S06), because names are not safe
identifiers. Foreign keys: ProjectID → projects, WorkerID → workers, SupplierID → suppliers.

**Why it is now 2NF.** Single-column keys cannot have partial dependencies. The equipment cost needs both
project and equipment (a Crane is 5000 on P001 and 5500 on P002). The material price needs project
(Steel Beams 500 vs 520) and material (Concrete 120 vs Steel 300). We also keep the supplier, because
prices are agreed with a supplier. The links table has no non-key columns.

**How I checked it.** `scripts/verify_2nf.py`: no duplicate rows or keys, values match the raw file,
no broken foreign keys, and joining the 6 tables gives back the 1NF file exactly. Nothing was lost.

**What is still wrong (lead-in to Ange).** projects.csv still repeats client and supervisor details.
Metro Corp's phone is stored twice and Sarah Lee's three times. That is a transitive dependency, fixed in 3NF.

---

## Likely questions

**Why not split into separate tables already in 1NF?**
1NF only asks for atomic values. Keeping one table shows the step clearly and makes the redundancy visible.
Splitting is what 2NF and 4NF are for.

**Isn't a smaller key possible?**
Only by coincidence in this sample (5 columns happen to be unique). A key must stay unique for any valid
data, and a second OSHA carpenter on P001 would break the smaller set. `scripts/verify_1nf_key.py` shows this.

**Does the price really need SupplierID?**
In this sample (ProjectID, MaterialSupplied) happens to be enough, because only P004 buys the same material
(Glass Panels) from two suppliers, and both charge 250. In practice each supplier quotes its own price,
so we keep SupplierID in the key.

**Why is project_resource_links still 280 rows?**
It keeps the combinations so the split is lossless. Its redundancy comes from multi-valued facts, which
4NF removes (Christian's part).

**Why surrogate keys instead of names?**
Two workers or companies can share a name, and names change. W01 never changes.
