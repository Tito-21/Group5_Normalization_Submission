# Send-back summary for Tito (3NF, BCNF and assumptions)

Paste this under Stage 3 and Stage 4, for example as a short "Verification" paragraph at the end of each.

---

**Verification, Stage 3 (Ange).** Joining projects with clients on ClientID and supervisors on SupervisorID
rebuilds `2NF/projects.csv` exactly (7 rows, no null foreign keys, no orphans), so the decomposition is lossless.
The five unchanged tables are identical to their 2NF versions.

**Verification, Stage 4 (Ange).** All four counterexamples hold in the CSV files (BuildPro sells Concrete and
Steel; P004 buys Glass Panels from S02 and S04; Sarah Lee runs Infrastructure and Commercial projects; Metro
Corp has two supervisors), and the BCNF folder is identical to the 3NF folder. A brute-force scan of every set
of up to 3 columns found a few dependencies that hold only by coincidence in this sample (for example
SiteCity -> SiteState and ClientID -> ProjectType). They are not business rules, so no table is split.

**Assumptions.** Agree with 2 to 5. Partly disagree with 1: in P001, P004 and P007 the worker-supplier pairs are
not a full cross-product (3 of 6, 2 of 4, 2 of 4), so the pairing carries some information that the final design
drops. Please decide: keep the design with a clearer note, or add `project_worker_supplier`. Also add the
assumption that names are unique candidate keys, and mention WorkerPhone and SupervisorPhone next to ClientPhone
in the BCNF key table.

Run the checks with `python3 scripts/verify_3nf_bcnf.py`.
