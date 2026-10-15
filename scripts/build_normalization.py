"""Builds the 1NF -> 2NF -> 3NF -> BCNF -> 4NF CSV files from the raw dataset.

Run from the project root:  python3 scripts/build_normalization.py
"""
import csv
import itertools
import os
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw_data", "big3_construction_raw_data.csv")


def write(stage, name, header, rows):
    folder = os.path.join(ROOT, stage)
    os.makedirs(folder, exist_ok=True)
    rows = list(rows)
    with open(os.path.join(folder, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{stage}/{name}: {len(rows)} rows")


def check_fd(rows, lhs, rhs, label):
    """Fail loudly if lhs -> rhs does not hold in the data."""
    seen = {}
    for r in rows:
        k = tuple(r[c] for c in lhs)
        v = tuple(r[c] for c in rhs)
        if seen.setdefault(k, v) != v:
            raise SystemExit(f"FD violated ({label}): {k} -> {seen[k]} vs {v}")


def unique(rows, cols):
    return list(OrderedDict.fromkeys(tuple(r[c] for c in cols) for r in rows))


with open(RAW, newline="") as f:
    raw = list(csv.DictReader(f))

# ---------------------------------------------------------------- 1NF
# Every multi-valued cell is split on "|". Material/cost and equipment/cost
# lists are positional pairs, so they are zipped before being expanded.
nf1_cols = [
    "ProjectID", "ProjectName", "ProjectType", "StartDate", "EndDate",
    "SiteAddress", "SiteCity", "SiteState",
    "ClientName", "ClientPhone", "ClientEmail", "ClientCity",
    "SupervisorName", "SupervisorPhone",
    "WorkerName", "WorkerPhone", "WorkerSkill", "WorkerCertification", "WorkerHourlyRate",
    "SupplierName", "SupplierCity", "SupplierPhone",
    "MaterialSupplied", "MaterialUnitCost", "EquipmentUsed", "EquipmentRentalCost",
]
nf1 = []
for r in raw:
    materials = list(zip(r["MaterialSupplied"].split("|"), r["MaterialUnitCost"].split("|"), strict=True))
    equipment = list(zip(r["EquipmentUsed"].split("|"), r["EquipmentRentalCost"].split("|"), strict=True))
    for skill, cert, phone, (mat, mcost), (eq, ecost) in itertools.product(
        r["WorkerSkills"].split("|"), r["WorkerCertifications"].split("|"),
        r["SupplierPhones"].split("|"), materials, equipment,
    ):
        row = {c: r.get(c, "") for c in nf1_cols}
        row.update(WorkerSkill=skill, WorkerCertification=cert, SupplierPhone=phone,
                   MaterialSupplied=mat, MaterialUnitCost=mcost,
                   EquipmentUsed=eq, EquipmentRentalCost=ecost)
        nf1.append(row)

nf1_key = ["ProjectID", "WorkerName", "WorkerSkill", "WorkerCertification",
           "SupplierName", "SupplierPhone", "MaterialSupplied", "EquipmentUsed"]
assert len(unique(nf1, nf1_key)) == len(nf1), "1NF key is not unique"
write("1NF", "construction_1nf.csv", nf1_cols, ([r[c] for c in nf1_cols] for r in nf1))

# Verify the functional dependencies the later stages rely on.
project_cols = ["ProjectName", "ProjectType", "StartDate", "EndDate", "SiteAddress", "SiteCity",
                "SiteState", "ClientName", "ClientPhone", "ClientEmail", "ClientCity",
                "SupervisorName", "SupervisorPhone"]
check_fd(nf1, ["ProjectID"], project_cols, "ProjectID -> project attributes")
check_fd(nf1, ["WorkerName"], ["WorkerPhone", "WorkerHourlyRate"], "WorkerName -> worker attributes")
check_fd(nf1, ["SupplierName"], ["SupplierCity"], "SupplierName -> SupplierCity")
check_fd(nf1, ["ProjectID", "SupplierName", "MaterialSupplied"], ["MaterialUnitCost"], "unit cost")
check_fd(nf1, ["ProjectID", "EquipmentUsed"], ["EquipmentRentalCost"], "rental cost")
check_fd(nf1, ["ClientName"], ["ClientPhone", "ClientEmail", "ClientCity"], "ClientName -> client attributes")
check_fd(nf1, ["SupervisorName"], ["SupervisorPhone"], "SupervisorName -> SupervisorPhone")


def counterexample(rows, lhs, rhs):
    """Return two rows that agree on lhs but differ on rhs, proving lhs -/-> rhs."""
    seen = {}
    for r in rows:
        k = tuple(r[c] for c in lhs)
        v = tuple(r[c] for c in rhs)
        if k in seen and seen[k] != v:
            return k, seen[k], v
        seen.setdefault(k, v)
    return None


# Candidate BCNF-breaking rules, each disproved by the data (used in the BCNF write-up).
for lhs, rhs in [
    (["SupplierName"], ["MaterialSupplied"]),
    (["ProjectID", "MaterialSupplied"], ["SupplierName"]),
    (["SupervisorName"], ["ProjectType"]),
    (["ClientName"], ["SupervisorName"]),
]:
    ce = counterexample(nf1, lhs, rhs)
    assert ce, f"{lhs} -> {rhs} unexpectedly holds"
    print(f"Not an FD: {' + '.join(lhs)} -> {rhs[0]}  e.g. {ce[0]} gives {ce[1][0]} and {ce[2][0]}")

# ---------------------------------------------------------------- surrogate keys
def make_ids(names, prefix, width=2):
    return {n: f"{prefix}{i:0{width}d}" for i, n in enumerate(names, 1)}

worker_id = make_ids([w for (w,) in unique(nf1, ["WorkerName"])], "W")
supplier_id = make_ids([s for (s,) in unique(nf1, ["SupplierName"])], "S")
client_id = make_ids([c for (c,) in unique(nf1, ["ClientName"])], "C")
supervisor_id = make_ids([s for (s,) in unique(nf1, ["SupervisorName"])], "SV")

# ---------------------------------------------------------------- 2NF
projects_2nf = (["ProjectID"] + project_cols, unique(nf1, ["ProjectID"] + project_cols))
workers = (["WorkerID", "WorkerName", "WorkerPhone", "WorkerHourlyRate"],
           [(worker_id[n], n, *rest) for n, *rest in unique(nf1, ["WorkerName", "WorkerPhone", "WorkerHourlyRate"])])
suppliers = (["SupplierID", "SupplierName", "SupplierCity"],
             [(supplier_id[n], n, c) for n, c in unique(nf1, ["SupplierName", "SupplierCity"])])
material_supply = (["ProjectID", "SupplierID", "MaterialSupplied", "MaterialUnitCost"],
                   [(p, supplier_id[s], m, c) for p, s, m, c in
                    unique(nf1, ["ProjectID", "SupplierName", "MaterialSupplied", "MaterialUnitCost"])])
equipment = (["ProjectID", "EquipmentUsed", "EquipmentRentalCost"],
             unique(nf1, ["ProjectID", "EquipmentUsed", "EquipmentRentalCost"]))
resource_links = (["ProjectID", "WorkerID", "WorkerSkill", "WorkerCertification",
                   "SupplierID", "SupplierPhone", "MaterialSupplied", "EquipmentUsed"],
                  [(p, worker_id[w], sk, ce, supplier_id[s], ph, m, e) for p, w, sk, ce, s, ph, m, e in
                   unique(nf1, nf1_key)])

shared = {
    "workers.csv": workers,
    "suppliers.csv": suppliers,
    "project_material_supply.csv": material_supply,
    "project_equipment.csv": equipment,
}
write("2NF", "projects.csv", *projects_2nf)
for name, table in shared.items():
    write("2NF", name, *table)
write("2NF", "project_resource_links.csv", *resource_links)

# ---------------------------------------------------------------- 3NF / BCNF
clients = (["ClientID", "ClientName", "ClientPhone", "ClientEmail", "ClientCity"],
           [(client_id[n], n, *rest) for n, *rest in
            unique(nf1, ["ClientName", "ClientPhone", "ClientEmail", "ClientCity"])])
supervisors = (["SupervisorID", "SupervisorName", "SupervisorPhone"],
               [(supervisor_id[n], n, ph) for n, ph in
                unique(nf1, ["SupervisorName", "SupervisorPhone"])])
projects_3nf = (["ProjectID", "ProjectName", "ProjectType", "StartDate", "EndDate",
                 "SiteAddress", "SiteCity", "SiteState", "ClientID", "SupervisorID"],
                [row[:8] + (client_id[row[8]], supervisor_id[row[12]]) for row in projects_2nf[1]])

for stage in ("3NF", "BCNF"):
    write(stage, "projects.csv", *projects_3nf)
    write(stage, "clients.csv", *clients)
    write(stage, "supervisors.csv", *supervisors)
    for name, table in shared.items():
        write(stage, name, *table)
    write(stage, "project_resource_links.csv", *resource_links)

# ---------------------------------------------------------------- 4NF
# project_resource_links is split along its independent multi-valued facts.
links = resource_links[1]
project_workers = sorted(set((p, w) for p, w, *_ in links))
skills = defaultdict(list)
certs = defaultdict(list)
phones = defaultdict(list)
for p, w, sk, ce, s, ph, m, e in links:
    if sk not in skills[w]:
        skills[w].append(sk)
    if ce not in certs[w]:
        certs[w].append(ce)
    if ph not in phones[s]:
        phones[s].append(ph)

write("4NF", "projects.csv", *projects_3nf)
write("4NF", "clients.csv", *clients)
write("4NF", "supervisors.csv", *supervisors)
for name, table in shared.items():
    write("4NF", name, *table)
write("4NF", "project_workers.csv", ["ProjectID", "WorkerID"], project_workers)
write("4NF", "worker_skills.csv", ["WorkerID", "Skill"],
      sorted((w, s) for w in skills for s in skills[w]))
write("4NF", "worker_certifications.csv", ["WorkerID", "Certification"],
      sorted((w, c) for w in certs for c in certs[w]))
write("4NF", "supplier_phones.csv", ["SupplierID", "SupplierPhone"],
      sorted((s, ph) for s in phones for ph in phones[s]))

# The (Project, Supplier, Material) and (Project, Equipment) projections of the
# links table must already be covered by the 2NF tables, so nothing is lost.
assert set((p, s, m) for p, _, _, _, s, _, m, _ in links) == set(r[:3] for r in material_supply[1])
assert set((p, e) for p, *_, e in links) == set(r[:2] for r in equipment[1])
print("All dependency and lossless-join checks passed.")
