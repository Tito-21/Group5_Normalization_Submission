import itertools

from verify_common import KEY_1NF, RAW, Report, holds, is_unique, load, split

PROJECT_COLS = ["ProjectName", "ProjectType", "StartDate", "EndDate", "SiteAddress", "SiteCity",
                "SiteState", "ClientName", "ClientPhone", "ClientEmail", "ClientCity",
                "SupervisorName", "SupervisorPhone"]
TABLES = {
    "projects": (["ProjectID"], 7),
    "workers": (["WorkerID"], 5),
    "suppliers": (["SupplierID"], 6),
    "project_material_supply": (["ProjectID", "SupplierID", "MaterialSupplied"], 16),
    "project_equipment": (["ProjectID", "EquipmentUsed"], 13),
    "project_resource_links": (["ProjectID", "WorkerID", "WorkerSkill", "WorkerCertification",
                                "SupplierID", "SupplierPhone", "MaterialSupplied", "EquipmentUsed"], 280),
}

raw = load(RAW)
nf1 = load("1NF/construction_1nf.csv")
t = {name: load(f"2NF/{name}.csv") for name in TABLES}
report = Report("2NF: 2NF/*.csv vs 1NF and raw data")

for lhs, rhs in [(["ProjectID"], PROJECT_COLS),
                 (["WorkerName"], ["WorkerPhone", "WorkerHourlyRate"]),
                 (["SupplierName"], ["SupplierCity"]),
                 (["ProjectID", "SupplierName", "MaterialSupplied"], ["MaterialUnitCost"]),
                 (["ProjectID", "EquipmentUsed"], ["EquipmentRentalCost"])]:
    report.check(f"partial dependency holds in 1NF: {' + '.join(lhs)} -> {', '.join(rhs)}",
                 holds(nf1, lhs, rhs))

for name, (pk, count) in TABLES.items():
    rows = t[name]
    report.check(f"{name}: {count} rows, no duplicate rows, primary key ({', '.join(pk)}) unique",
                 len(rows) == count and is_unique(rows, list(rows[0])) and is_unique(rows, pk),
                 f"{len(rows)} rows")

for name, col in [("projects", "ProjectName"), ("workers", "WorkerName"), ("suppliers", "SupplierName")]:
    report.check(f"{name}: {col} is unique, so the surrogate key maps 1:1 to a name",
                 is_unique(t[name], [col]))

supplier_name = {r["SupplierID"]: r["SupplierName"] for r in t["suppliers"]}
expected = {
    "projects": {tuple(r[c] for c in ["ProjectID"] + PROJECT_COLS) for r in raw},
    "workers": {(r["WorkerName"], r["WorkerPhone"], r["WorkerHourlyRate"]) for r in raw},
    "suppliers": {(r["SupplierName"], r["SupplierCity"]) for r in raw},
    "project_material_supply": {(r["ProjectID"], r["SupplierName"], m, c) for r in raw
                                for m, c in zip(split(r["MaterialSupplied"]), split(r["MaterialUnitCost"]))},
    "project_equipment": {(r["ProjectID"], e, c) for r in raw
                          for e, c in zip(split(r["EquipmentUsed"]), split(r["EquipmentRentalCost"]))},
}
actual = {
    "projects": {tuple(r.values()) for r in t["projects"]},
    "workers": {(r["WorkerName"], r["WorkerPhone"], r["WorkerHourlyRate"]) for r in t["workers"]},
    "suppliers": {(r["SupplierName"], r["SupplierCity"]) for r in t["suppliers"]},
    "project_material_supply": {(r["ProjectID"], supplier_name[r["SupplierID"]], r["MaterialSupplied"],
                                 r["MaterialUnitCost"]) for r in t["project_material_supply"]},
    "project_equipment": {tuple(r.values()) for r in t["project_equipment"]},
}
for name in expected:
    report.check(f"{name}: values match the raw file exactly", expected[name] == actual[name])

P = {r["ProjectID"]: r for r in t["projects"]}
W = {r["WorkerID"]: r for r in t["workers"]}
S = {r["SupplierID"]: r for r in t["suppliers"]}
M = {(r["ProjectID"], r["SupplierID"], r["MaterialSupplied"]): r["MaterialUnitCost"]
     for r in t["project_material_supply"]}
E = {(r["ProjectID"], r["EquipmentUsed"]): r["EquipmentRentalCost"] for r in t["project_equipment"]}

links = t["project_resource_links"]
report.check("foreign keys: every ProjectID, WorkerID and SupplierID points to an existing row",
             all(r["ProjectID"] in P and r["WorkerID"] in W and r["SupplierID"] in S for r in links)
             and all(r["ProjectID"] in P and r["SupplierID"] in S for r in t["project_material_supply"])
             and all(r["ProjectID"] in P for r in t["project_equipment"]))
report.check("every link row has a matching material price and equipment cost",
             all((r["ProjectID"], r["SupplierID"], r["MaterialSupplied"]) in M
                 and (r["ProjectID"], r["EquipmentUsed"]) in E for r in links))

rebuilt = set()
for r in links:
    row = dict(P[r["ProjectID"]])
    w, s = W[r["WorkerID"]], S[r["SupplierID"]]
    row.update(WorkerName=w["WorkerName"], WorkerPhone=w["WorkerPhone"], WorkerHourlyRate=w["WorkerHourlyRate"],
               WorkerSkill=r["WorkerSkill"], WorkerCertification=r["WorkerCertification"],
               SupplierName=s["SupplierName"], SupplierCity=s["SupplierCity"], SupplierPhone=r["SupplierPhone"],
               MaterialSupplied=r["MaterialSupplied"],
               MaterialUnitCost=M[(r["ProjectID"], r["SupplierID"], r["MaterialSupplied"])],
               EquipmentUsed=r["EquipmentUsed"], EquipmentRentalCost=E[(r["ProjectID"], r["EquipmentUsed"])])
    rebuilt.add(tuple(row[c] for c in nf1[0]))
report.check("lossless: joining the 6 tables rebuilds the 1NF file row for row",
             rebuilt == {tuple(r.values()) for r in nf1})

for name, value in [("project_material_supply", "MaterialUnitCost"), ("project_equipment", "EquipmentRentalCost")]:
    pk = TABLES[name][0]
    for part in itertools.chain.from_iterable(itertools.combinations(pk, n) for n in range(1, len(pk))):
        if holds(t[name], list(part), [value]):
            report.note(f"{name}: {' + '.join(part)} happens to determine {value} in this sample "
                        f"(coincidence, see reviews/cedric/findings_and_corrections.md)")
        else:
            report.check(f"{name}: {' + '.join(part)} alone does not determine {value}", True)

report.check("project_resource_links keeps the 1NF key, with names swapped for WorkerID/SupplierID",
             KEY_1NF == [c.replace("ID", "Name") if c in ("WorkerID", "SupplierID") else c
                         for c in TABLES["project_resource_links"][0]])
report.finish()
