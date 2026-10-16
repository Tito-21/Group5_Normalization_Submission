import itertools

from verify_common import KEY_1NF, Report, is_unique, load

nf1 = load("1NF/construction_1nf.csv")
report = Report("1NF key: is the 8-column key the smallest unique set?")

report.check("the 8-column key is unique", is_unique(nf1, KEY_1NF))
for col in KEY_1NF:
    rest = [c for c in KEY_1NF if c != col]
    if is_unique(nf1, rest):
        report.note(f"still unique without {col}")

minimal = []
for n in range(1, len(KEY_1NF) + 1):
    for cols in itertools.combinations(KEY_1NF, n):
        if is_unique(nf1, cols) and not any(set(m) <= set(cols) for m in minimal):
            minimal.append(cols)
for cols in minimal:
    report.note(f"smallest unique set in this sample ({len(cols)} columns): {', '.join(cols)}")

mike = next(r for r in nf1 if r["ProjectID"] == "P001" and r["WorkerName"] == "Mike Ross")
second_carpenter = dict(mike, WorkerName="New Carpenter", WorkerPhone="617-555-3999")
sample = nf1 + [second_carpenter]
report.note("test: add a second OSHA-certified carpenter to P001 (same skill, cert, supplier, material, equipment)")
for cols in minimal:
    report.check(f"  the {len(cols)}-column set now has duplicates, so it was unique only by chance",
                 not is_unique(sample, cols))
report.check("  the 8-column key is still unique, so it is the correct key",
             is_unique(sample, KEY_1NF))
report.finish()
