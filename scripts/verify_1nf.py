import math

from verify_common import KEY_1NF, RAW, Report, is_unique, load, split

LISTS = {"WorkerSkills": "WorkerSkill",
         "WorkerCertifications": "WorkerCertification",
         "SupplierPhones": "SupplierPhone"}
PAIRS = [("MaterialSupplied", "MaterialUnitCost"), ("EquipmentUsed", "EquipmentRentalCost")]
PAIRED_COLS = {c for pair in PAIRS for c in pair}

raw = load(RAW)
nf1 = load("1NF/construction_1nf.csv")
report = Report("1NF: 1NF/construction_1nf.csv vs raw data")

expected_header = [LISTS.get(c, c) for c in raw[0]]
report.check("columns are the raw columns, list columns renamed to singular",
             list(nf1[0]) == expected_header)
report.check("every cell holds one non-empty value with no '|' and no stray spaces",
             all(v and v == v.strip() and "|" not in v for r in nf1 for v in r.values()))

total = 0
for n, r in enumerate(raw, 1):
    rows =[x for x in nf1 if x["ProjectID"] == r["ProjectID"] and x["WorkerName"] == r["WorkerName"]]
    sizes = [len(split(r[c])) for c in LISTS] + [len(split(r[a])) for a, _ in PAIRS]
    expected = math.prod(sizes)
    total += expected

    problems = [f"{a} and {b} lists differ in length" for a, b in PAIRS
                if len(split(r[a])) != len(split(r[b]))]
    if len(rows) != expected:
        problems.append(f"{len(rows)} rows")
    for src, dst in LISTS.items():
        if {x[dst] for x in rows} != set(split(r[src])):
            problems.append(f"{dst} values differ")
    for a, b in PAIRS:
        if {(x[a], x[b]) for x in rows} != set(zip(split(r[a]), split(r[b]))):
            problems.append(f"{a}/{b} pairs differ")
    if any(x[c] != r[c] for x in rows for c in r if c in x and c not in PAIRED_COLS):
        problems.append("single-valued columns changed")

    report.check(f"raw row {n:2} {r['ProjectID']} {r['WorkerName']:<15} "
                 f"{'x'.join(map(str, sizes))} = {expected:2} rows, values and cost pairs match",
                 not problems, ", ".join(problems))

report.check(f"total rows = sum of expected rows ({total})", len(nf1) == total, f"found {len(nf1)}")
report.check("no two rows are identical", is_unique(nf1, list(nf1[0])))
report.check("8-column primary key is unique", is_unique(nf1, KEY_1NF))
report.check("Downtown Plaza is repeated on 72 rows (figure used in the document)",
             sum(x["ProjectName"] == "Downtown Plaza" for x in nf1) == 72)
report.finish()
