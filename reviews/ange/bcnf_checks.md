# BCNF checks

Checked by `scripts/verify_3nf_bcnf.py`.

## The four counterexamples

| Rule tested | Counterexample | Found in the files |
|---|---|---|
| SupplierID -> MaterialSupplied | BuildPro (S01) sells Concrete and Steel on P001, Bricks and Cement on P003 | Yes, 4 rows for S01 in project_material_supply.csv |
| (ProjectID, MaterialSupplied) -> SupplierID | P004 buys Glass Panels from S02 and S04 | Yes, 2 rows |
| SupervisorID -> ProjectType | Sarah Lee (SV02): P002 and P007 Infrastructure, P005 Commercial | Yes, in projects.csv |
| ClientID -> SupervisorID | Metro Corp (C01): P001 has SV01, P005 has SV02 | Yes, in projects.csv |

All four rules fail on real data, so none of them can cause a BCNF violation.

## BCNF folder

`BCNF/` has the same 8 files as `3NF/`, byte for byte, which matches "no decomposition was needed".

## Extra scan: dependencies that hold only by coincidence

The script tests every set of 1 to 3 columns as a determinant and lists every dependency that happens to
hold in the data while the determinant is not a key. These are the only ones:

| Table | Dependency | Why we do not treat it as a rule |
|---|---|---|
| projects | SiteCity -> SiteState and SiteState -> SiteCity | Names repeat across states (Assumption 5). Only 7 projects |
| projects | ClientID -> ProjectType | Each client has one project type in the sample (Metro: Commercial, City Transit: Infrastructure, Retail: Residential). A client can commission any type |
| project_material_supply | MaterialUnitCost -> MaterialSupplied | Every price in the sample belongs to one material. A price is not an identity |
| project_material_supply | (ProjectID, MaterialSupplied) -> MaterialUnitCost | Only P004 buys one material from two suppliers, and both charge 250 (already in the document) |
| project_resource_links | 17 dependencies | All-key table with 280 combinations of independent lists. Same reason as Assumption 4 |

If someone asked us to treat any of these as business rules, the table would need splitting.
Nothing in the data says they are rules, so the decision in the document stays: no table violates BCNF.

**Result: Stage 4 is correct.** The document does not list these coincidences, so one sentence could be added (see
[send_back_summary.md](send_back_summary.md)).
