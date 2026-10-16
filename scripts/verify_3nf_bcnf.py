import filecmp
import itertools
import os

from verify_common import ROOT, Report, holds, is_unique, load

PROJECT_COLS = ["ProjectName", "ProjectType", "StartDate", "EndDate", "SiteAddress", "SiteCity",
                "SiteState", "ClientName", "ClientPhone", "ClientEmail", "ClientCity",
                "SupervisorName", "SupervisorPhone"]
TABLES = {  # 3NF table -> (primary key, expected rows)
    "projects": (["ProjectID"], 7),
    "clients": (["ClientID"], 4),
    "supervisors": (["SupervisorID"], 3),
    "workers": (["WorkerID"], 5),
    "suppliers": (["SupplierID"], 6),
    "project_material_supply": (["ProjectID", "SupplierID", "MaterialSupplied"], 16),
    "project_equipment": (["ProjectID", "EquipmentUsed"], 13),
    "project_resource_links": (["ProjectID", "WorkerID", "WorkerSkill", "WorkerCertification",
                                "SupplierID", "SupplierPhone", "MaterialSupplied", "EquipmentUsed"], 280),
}

t = {name: load(f"3NF/{name}.csv") for name in TABLES}
p2 = load("2NF/projects.csv")
report = Report("3NF and BCNF: 3NF/*.csv and BCNF/*.csv vs 2NF and raw data")

# 3NF: the transitive dependencies really exist in 2NF, and the split is lossless
report.check("transitive: ClientName -> ClientPhone, ClientEmail, ClientCity holds in 2NF/projects",
             holds(p2, ["ClientName"], ["ClientPhone", "ClientEmail", "ClientCity"]))
report.check("transitive: SupervisorName -> SupervisorPhone holds in 2NF/projects",
             holds(p2, ["SupervisorName"], ["SupervisorPhone"]))
report.check("ClientName is not a key of 2NF/projects (it repeats), so the dependency is transitive",
             not is_unique(p2, ["ClientName"]))
report.check("SupervisorName is not a key of 2NF/projects (it repeats)",
             not is_unique(p2, ["SupervisorName"]))

clients = {r["ClientID"]: r for r in t["clients"]}
sups = {r["SupervisorID"]: r for r in t["supervisors"]}
orphans = [r["ProjectID"] for r in t["projects"]
           if r["ClientID"] not in clients or r["SupervisorID"] not in sups]
report.check("every projects.ClientID and SupervisorID exists in its parent table", not orphans, str(orphans))

joined = []
for r in t["projects"]:
    c, s = clients[r["ClientID"]], sups[r["SupervisorID"]]
    joined.append({"ProjectID": r["ProjectID"], **{k: r[k] for k in PROJECT_COLS[:7]},
                   "ClientName": c["ClientName"], "ClientPhone": c["ClientPhone"],
                   "ClientEmail": c["ClientEmail"], "ClientCity": c["ClientCity"],
                   "SupervisorName": s["SupervisorName"], "SupervisorPhone": s["SupervisorPhone"]})
cols = ["ProjectID"] + PROJECT_COLS
report.check("projects JOIN clients JOIN supervisors rebuilds 2NF/projects.csv exactly",
             sorted(tuple(r[c] for c in cols) for r in joined) == sorted(tuple(r[c] for c in cols) for r in p2))

for name, (pk, count) in TABLES.items():
    rows = t[name]
    report.check(f"{name}: {count} rows, no duplicate rows, primary key ({', '.join(pk)}) unique",
                 len(rows) == count and is_unique(rows, list(rows[0])) and is_unique(rows, pk), f"{len(rows)} rows")
for name in ["workers", "suppliers", "project_material_supply", "project_equipment", "project_resource_links"]:
    report.check(f"{name}.csv is unchanged from 2NF", filecmp.cmp(f"{ROOT}/2NF/{name}.csv", f"{ROOT}/3NF/{name}.csv", shallow=False))
report.check("clients: ClientName and ClientEmail are unique (alternate keys)",
             is_unique(t["clients"], ["ClientName"]) and is_unique(t["clients"], ["ClientEmail"]))

# BCNF: the four counterexamples from the document
pms, proj = t["project_material_supply"], t["projects"]
report.check("counterexample: SupplierID -> MaterialSupplied does NOT hold (S01 sells Concrete and Steel)",
             not holds(pms, ["SupplierID"], ["MaterialSupplied"]))
report.check("counterexample: (ProjectID, MaterialSupplied) -> SupplierID does NOT hold (P004 Glass Panels)",
             not holds(pms, ["ProjectID", "MaterialSupplied"], ["SupplierID"]))
report.check("counterexample: SupervisorID -> ProjectType does NOT hold (SV02)",
             not holds(proj, ["SupervisorID"], ["ProjectType"]))
report.check("counterexample: ClientID -> SupervisorID does NOT hold (C01)",
             not holds(proj, ["ClientID"], ["SupervisorID"]))
glass = sorted(r["SupplierID"] for r in pms if r["ProjectID"] == "P004" and r["MaterialSupplied"] == "Glass Panels")
report.check("P004 buys Glass Panels from S02 and S04", glass == ["S02", "S04"], str(glass))

# BCNF folder equals 3NF folder
same = all(filecmp.cmp(f"{ROOT}/3NF/{n}.csv", f"{ROOT}/BCNF/{n}.csv", shallow=False) for n in TABLES)
report.check("BCNF/ holds the same 8 files as 3NF/, byte for byte",
             same and sorted(os.listdir(f"{ROOT}/BCNF")) == sorted(f"{n}.csv" for n in TABLES))

# Brute-force BCNF scan: any FD X -> A that holds in the data but where X is not a superkey
for name, (pk, _) in TABLES.items():
    rows = t[name]
    cols = list(rows[0])
    found = []
    for size in (1, 2, 3):
        for lhs in itertools.combinations(cols, size):
            if is_unique(rows, list(lhs)):
                continue  # superkey, always allowed
            for a in cols:
                if a in lhs or any(set(f[0]) <= set(lhs) and f[1] == a for f in found):
                    continue
                if holds(rows, list(lhs), [a]):
                    found.append((lhs, a))
    if name == "project_resource_links":
        report.note(f"{name}: {len(found)} FDs hold by coincidence with a non-key determinant "
                    f"(all-key table; see BCNF doc and Assumption 4)")
    else:
        for lhs, a in found:
            report.note(f"{name}: {' + '.join(lhs)} -> {a} holds in the data but the determinant is not a key")
        if not found:
            report.note(f"{name}: no FD with a non-key determinant (size 1-3)")
report.finish()
