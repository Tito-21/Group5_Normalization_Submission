# Findings and corrected wording for Stage 1 and Stage 2

The CSV files are correct. Two sentences in `normalization_explanation.docx` need changing,
because a marker could check them against the data and find them false.

---

## Finding 1: Stage 1, "What key identifies each row?"

**Current text:**

> No smaller set is unique. Removing any one of these columns produces duplicate key values (the script checks this).

**Problem:** both claims are false.

- `build_normalization.py` only checks that the 8-column key is unique. It never tests smaller sets.
- In the 280 rows, dropping ProjectID, WorkerName or SupplierName on its own still leaves every row unique.
  Just 5 columns (WorkerSkill, WorkerCertification, SupplierPhone, MaterialSupplied, EquipmentUsed)
  are enough in this sample (`scripts/verify_1nf_key.py`).

**Why the 8-column key is still right:** the 5-column set is unique only by chance. If a second
OSHA-certified carpenter joined P001 and was listed with BuildPro like Mike Ross, their rows would match Mike Ross's on all 5 columns and only
WorkerName would tell them apart. The script runs this exact test: the 5-column set breaks and the
8-column key still holds.

**Why it matters:** the 2NF section calls ProjectID → ProjectName a *partial* dependency. That is only
true if ProjectID is part of the key, so the key has to be justified by meaning, not by the sample.

**Replace with:**

> We chose this key from what a row means: one skill and one certification of one worker on one
> project, combined with one phone, one material and one piece of equipment of one supplier. In this
> 15-project sample a smaller set of columns happens to be unique (for example, the five split columns
> alone). That is a coincidence: a second OSHA-certified carpenter on P001, listed with BuildPro like
> Mike Ross, would produce rows identical to his on those five columns. A key must stay unique for any valid data, so all 8 columns are
> needed. Our verification script tests this case.

---

## Finding 2: Stage 2, "Why is the design now in 2NF?"

**Current text:**

> In project_material_supply, MaterialUnitCost needs all three key columns, because the same material
> has different prices for different projects and suppliers.

**Problem:** the data proves this for projects but not for suppliers.

| Remove from the key | Still determines the cost? | Evidence |
|---|---|---|
| ProjectID → (SupplierID, MaterialSupplied) | No | SteelWorks charges 500 for Steel Beams on P001 and P004, 520 on P007 |
| MaterialSupplied → (ProjectID, SupplierID) | No | BuildPro charges 120 for Concrete and 300 for Steel on P001 |
| SupplierID → (ProjectID, MaterialSupplied) | **Yes, in this sample** | The only project buying one material from two suppliers is P004 (Glass Panels), and both charge 250 |

The BCNF section already says (ProjectID, MaterialSupplied) → MaterialUnitCost "happens to hold in this
sample". The 2NF section should say the same thing, so the two sections don't contradict each other.

**Replace with:**

> In project_material_supply, MaterialUnitCost needs all three key columns. Without ProjectID the price
> is not fixed (SteelWorks charges 500 for Steel Beams on P001 and P004 but 520 on P007). Without
> MaterialSupplied it is not fixed either (BuildPro charges 120 for Concrete and 300 for Steel on P001).
> Without SupplierID the sample happens to work, because the only material bought from two suppliers
> (Glass Panels on P004) costs 250 from both. We keep SupplierID because a price is agreed with a
> supplier, so two suppliers can quote different prices for the same material on the same project
> (see BCNF, "Other dependencies we considered").

Ange reviews the BCNF section, so this sentence was checked against what that section already says.

---

## Checked and correct (no change needed)

- Stage 1: the 7 violating columns, zipping material/cost and equipment/cost by position, "new rows only",
  15 → 280 rows, 32 rows for raw row 1, Downtown Plaza on 72 rows.
- Stage 2: the partial-dependency table, the 6 files and their row counts, the surrogate keys
  W01–W05 and S01–S06, every foreign key listed, and "project_resource_links has no non-key columns".
- `build_normalization.py` rebuilds exactly the committed CSVs, and the zip holds the same CSVs and .docx.

## Not checked

- Whether `normalization_explanation.pdf` matches the current .docx word for word (no PDF text tool on this machine).
  The PDF must be exported again after the two corrections anyway.
