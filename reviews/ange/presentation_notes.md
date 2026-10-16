# Presentation notes: Stage 3 (3NF) and Stage 4 (BCNF)

About 3 to 4 minutes. Show `3NF/projects.csv` next to `clients.csv`, then the BCNF counterexample table.

---

## Stage 3: Third Normal Form

**The rule.** In 2NF, and no non-key column depends on another non-key column. Every column depends on the key,
the whole key and nothing but the key.

**The problem.** In `projects`, ProjectID -> ClientName -> ClientPhone, ClientEmail, ClientCity, and
ProjectID -> SupervisorName -> SupervisorPhone. Metro Corp runs P001 and P005, so its phone was stored twice.

**What we did.** New tables `clients` (ClientID, C01-C04) and `supervisors` (SupervisorID, SV01-SV03).
`projects` keeps only ClientID and SupervisorID as foreign keys.

**How I checked it.** Joining the three tables rebuilds `2NF/projects.csv` exactly. Nothing was lost.

**Why it is 3NF.** The other tables already depend directly on their keys. SiteCity -> SiteState was
rejected (Assumption 5).

---

## Stage 4: BCNF

**The rule.** For every dependency X -> Y, X must be a candidate key. 3NF allows an exception when Y is part of
a key. BCNF does not.

**What we checked.** Every dependency in every table, and the closure of every determinant. Every determinant
is a candidate key, so **no table violated BCNF and nothing was split.** The BCNF folder is the same as 3NF.

**The four rules we tested** (all fail on real data):
- A supplier sells one material: BuildPro sells Concrete and Steel.
- A project buys each material from one supplier: P004 buys Glass Panels from SteelWorks and Global Glass.
- A supervisor runs one project type: Sarah Lee runs Infrastructure and Commercial.
- A client has one supervisor: Metro Corp has John Carter and Sarah Lee.

**What is still wrong (lead-in to Christian).** `project_resource_links` is in BCNF but has 280 rows of
redundancy, from multi-valued dependencies. 4NF fixes that.

---

## Likely questions

**3NF vs BCNF?** 3NF allows a dependency if the dependent column is part of a key. BCNF requires the
determinant to be a key, always. They only differ in tables with overlapping composite candidate keys.

**Why no city/state table?** City names repeat across states (Portland, OR and Portland, ME). It only holds in
our 7 projects.

**SupplierPhone -> SupplierID holds in your data. Isn't that a violation?** Phones are not identifiers (Assumption 4).
If the business said phones are unique, `supplier_phones` would get an alternate key and stay in BCNF.

**Your scan found dependencies that hold. Why ignore them?** They hold only by coincidence in 7 projects
(for example, each client has one project type). A rule must hold for any valid data. Nothing says a client
cannot commission a different type.

**Are names really unique?** An assumption for this dataset. In a real database the surrogate IDs are the
primary keys and names get UNIQUE constraints.

**Is the worker-supplier pairing meaningful?** We treat it as a flattening artifact, but the pairs are not a
full cross-product in P001, P004 and P007, so it is a judgment call. An optional `project_worker_supplier`
table would keep it.
