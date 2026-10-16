# Review of the assumptions (section 1.8)

| # | Assumption | Verdict |
|---|---|---|
| 1 | A worker and a supplier on the same row are not related | **Partly disagree** |
| 2 | Skills and certifications belong to the worker | Agree |
| 3 | Equipment is used by the project | Agree, with a caveat |
| 4 | Phone numbers are contact details, not identifiers | Agree |
| 5 | City does not determine state in general | Agree |

## 1. Worker and supplier unrelated: partly disagree

The document says the pairing "never means anything consistent". That is only partly true.

- **For the document's view:** Mike Ross is paired with a different supplier on each of his 4 projects, and
  materials and equipment follow the supplier, not the worker.
- **Against it:** if workers and suppliers were independent within a project, flattening the file would give
  every worker-supplier combination. That is true for the 4 projects with one supplier. It is not true for
  the 3 projects with two suppliers:

| Project | Workers | Suppliers | Possible pairs | Pairs in the data |
|---|---|---|---|---|
| P001 | 3 | 2 | 6 | 3 |
| P004 | 2 | 2 | 4 | 2 |
| P007 | 2 | 2 | 4 | 2 |

So the pairing carries some information, and our final design (`project_workers` has no supplier column)
drops it. The document's last sentence covers this risk, but the final tables do not.

**Options for the group:**
1. Keep the design and say in 1.8 that this is a judgment call and that the pairs are not a full cross-product.
2. Add an optional table `project_worker_supplier(ProjectID, WorkerID, SupplierID)` with 15 rows.
   It is in 4NF because the pairs are not a cross-product, so there is no multi-valued dependency to split.
3. Ask the lecturer.

## 2. Skills and certifications belong to the worker: agree

Each worker's per-row lists are slices of one set, so the union is sensible: Mike Ross = Carpentry,
Concrete, Framing; Tom Hardy = Carpentry, Concrete, Steel Fixing, Welding. Harvey's "Project Management"
and "Management" are probably the same skill (already in the data-quality notes).

## 3. Equipment is used by the project: agree, with a caveat

Costs are consistent per (project, equipment), so no cost is lost. But the equipment set differs by supplier
row in P001, P004 and P007 (Bulldozer is only on BuildPro's rows in P001). Project-level equipment keeps every
item but loses the row it appeared on. This is the same issue as assumption 1.

## 4. Phones are not identifiers: agree

WorkerPhone and SupervisorPhone are also unique in the sample, like ClientPhone. The document mentions only
ClientPhone as a possible key, so one sentence should make it consistent. BCNF is not affected, because a
phone would be a key.

## 5. City does not determine state: agree

SiteCity -> SiteState does hold in the sample (and so does SiteAddress -> city and state). A marker could call
it a transitive dependency. The reasoning in the document (Portland, OR vs Portland, ME) is the defence.

## Missing assumption

We treat names (project, worker, client, supplier, supervisor) as unique candidate keys. Add this to 1.8.
