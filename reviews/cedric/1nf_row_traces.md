# 1NF row traces: raw rows 1, 9 and 15

Row numbers count data rows only (row 1 = line 2 of the raw CSV, under the header).
Each trace checks three things from the task sheet:

- every skill, certification, phone, material and equipment value appears, and nothing extra does
- each material and each piece of equipment keeps its **own** cost
- the number of 1NF rows equals the product of the list sizes

All 15 raw rows were checked the same way by `scripts/verify_1nf.py`. These three are written out by hand.

---

## Raw row 1: P001, Mike Ross

| Raw column | Raw value | Values after split |
|---|---|---|
| WorkerSkills | `Carpentry\|Framing` | 2 |
| WorkerCertifications | `OSHA\|First Aid` | 2 |
| SupplierPhones | `617-555-9000\|617-555-9001` | 2 |
| MaterialSupplied + MaterialUnitCost | `Concrete\|Steel` + `120\|300` | 2 pairs: (Concrete, 120), (Steel, 300) |
| EquipmentUsed + EquipmentRentalCost | `Crane\|Bulldozer` + `5000\|3000` | 2 pairs: (Crane, 5000), (Bulldozer, 3000) |

**Expected rows:** 2 × 2 × 2 × 2 × 2 = **32**. **Found in 1NF:** 32.

The first 8 rows (Carpentry + OSHA):

| WorkerSkill | WorkerCertification | SupplierPhone | MaterialSupplied | MaterialUnitCost | EquipmentUsed | EquipmentRentalCost |
|---|---|---|---|---|---|---|
| Carpentry | OSHA | 617-555-9000 | Concrete | 120 | Crane | 5000 |
| Carpentry | OSHA | 617-555-9000 | Concrete | 120 | Bulldozer | 3000 |
| Carpentry | OSHA | 617-555-9000 | Steel | 300 | Crane | 5000 |
| Carpentry | OSHA | 617-555-9000 | Steel | 300 | Bulldozer | 3000 |
| Carpentry | OSHA | 617-555-9001 | Concrete | 120 | Crane | 5000 |
| Carpentry | OSHA | 617-555-9001 | Concrete | 120 | Bulldozer | 3000 |
| Carpentry | OSHA | 617-555-9001 | Steel | 300 | Crane | 5000 |
| Carpentry | OSHA | 617-555-9001 | Steel | 300 | Bulldozer | 3000 |

The same 8 rows repeat for Carpentry + First Aid, Framing + OSHA and Framing + First Aid (4 × 8 = 32).

- Skills found: Carpentry, Framing. Certifications: OSHA, First Aid. Phones: 617-555-9000, 617-555-9001. Nothing extra.
- Concrete is always 120 and Steel is always 300. "Concrete = 300" never appears.
- Crane is always 5000 and Bulldozer is always 3000.
- Project, client, supervisor, worker phone/rate and supplier name/city are copied unchanged on all 32 rows.

**Result: correct.**

---

## Raw row 9: P004, Louis Litt

| Raw column | Raw value | Values after split |
|---|---|---|
| WorkerSkills | `Accounting\|Procurement` | 2 |
| WorkerCertifications | `MBA\|First Aid` | 2 |
| SupplierPhones | `206-555-6000` | 1 |
| MaterialSupplied + MaterialUnitCost | `Glass Panels` + `250` | 1 pair |
| EquipmentUsed + EquipmentRentalCost | `Lift` + `2000` | 1 pair |

**Expected rows:** 2 × 2 × 1 × 1 × 1 = **4**. **Found in 1NF:** 4.

| WorkerSkill | WorkerCertification | SupplierPhone | MaterialSupplied | MaterialUnitCost | EquipmentUsed | EquipmentRentalCost |
|---|---|---|---|---|---|---|
| Accounting | MBA | 206-555-6000 | Glass Panels | 250 | Lift | 2000 |
| Accounting | First Aid | 206-555-6000 | Glass Panels | 250 | Lift | 2000 |
| Procurement | MBA | 206-555-6000 | Glass Panels | 250 | Lift | 2000 |
| Procurement | First Aid | 206-555-6000 | Glass Panels | 250 | Lift | 2000 |

Supplier is Global Glass Co (Seattle) on all 4 rows. **Result: correct.**

---

## Raw row 15: P007, Harvey Specter

| Raw column | Raw value | Values after split |
|---|---|---|
| WorkerSkills | `Management\|Planning` | 2 |
| WorkerCertifications | `PMP\|OSHA` | 2 |
| SupplierPhones | `305-555-7000` | 1 |
| MaterialSupplied + MaterialUnitCost | `Rebar` + `210` | 1 pair |
| EquipmentUsed + EquipmentRentalCost | `Excavator` + `4200` | 1 pair |

**Expected rows:** 2 × 2 × 1 × 1 × 1 = **4**. **Found in 1NF:** 4.

| WorkerSkill | WorkerCertification | SupplierPhone | MaterialSupplied | MaterialUnitCost | EquipmentUsed | EquipmentRentalCost |
|---|---|---|---|---|---|---|
| Management | PMP | 305-555-7000 | Rebar | 210 | Excavator | 4200 |
| Management | OSHA | 305-555-7000 | Rebar | 210 | Excavator | 4200 |
| Planning | PMP | 305-555-7000 | Rebar | 210 | Excavator | 4200 |
| Planning | OSHA | 305-555-7000 | Rebar | 210 | Excavator | 4200 |

Supplier is Oceanic Materials (Miami) on all 4 rows. Rebar costs 210 here, not 200 as on P002, so the
cost was taken from this row and not from another project. **Result: correct.**

---

## All 15 rows

| Raw row | Project | Worker | Expected | Found |
|---|---|---|---|---|
| 1 | P001 | Mike Ross | 2×2×2×2×2 = 32 | 32 |
| 2 | P001 | Rachel Zane | 2×2×2×2×2 = 32 | 32 |
| 3 | P001 | Harvey Specter | 2×2×2×1×1 = 8 | 8 |
| 4 | P002 | Mike Ross | 2×2×1×2×2 = 16 | 16 |
| 5 | P002 | Tom Hardy | 2×2×1×2×2 = 16 | 16 |
| 6 | P003 | Rachel Zane | 2×2×2×2×2 = 32 | 32 |
| 7 | P003 | Tom Hardy | 2×2×2×2×2 = 32 | 32 |
| 8 | P004 | Mike Ross | 2×2×2×2×2 = 32 | 32 |
| 9 | P004 | Louis Litt | 2×2×1×1×1 = 4 | 4 |
| 10 | P005 | Harvey Specter | 2×2×1×2×2 = 16 | 16 |
| 11 | P005 | Rachel Zane | 2×2×1×2×2 = 16 | 16 |
| 12 | P006 | Tom Hardy | 2×2×1×1×1 = 4 | 4 |
| 13 | P006 | Mike Ross | 2×2×1×1×1 = 4 | 4 |
| 14 | P007 | Louis Litt | 2×2×2×2×2 = 32 | 32 |
| 15 | P007 | Harvey Specter | 2×2×1×1×1 = 4 | 4 |
| | | | **280** | **280** |

Order of the factors: skills × certifications × supplier phones × materials × equipment.
