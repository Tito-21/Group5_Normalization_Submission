# Group 5 – Normalization assignment: your tasks

Tito has built the full submission: all CSV files for 1NF → 4NF and the explanation document
(`normalization_explanation.docx`). Each of you now owns one part: check it, improve it if
something is wrong, and be ready to present it. Each task takes about 30–60 minutes.

Send your result to Tito by **[deadline]** so it can go into the final zip.

---

## Cedric – 1NF & 2NF verification

1. Open `raw_data/big3_construction_raw_data.csv` and `1NF/construction_1nf.csv`.
2. Pick 3 raw rows (suggestion: row 1, row 9, row 15). For each one, find its rows in the 1NF file
   and confirm that:
   - every skill, certification, phone, material and equipment value appears, and nothing extra does
   - each material still has its **own** cost (Concrete = 120 on P001, not 300)
   - the number of rows matches the multiplication (row 1 → 2×2×2×2×2 = 32 rows)
3. In the 2NF folder, check that `projects`, `workers`, `suppliers`, `project_material_supply` and
   `project_equipment` contain no duplicate rows, and that their values match the raw file.
4. **Send back:** 3–5 sentences describing what you checked and what you found (problems too).
   This goes into the document under the 1NF/2NF sections.
5. **Presentation:** explain 1NF and 2NF (document sections “Stage 1” and “Stage 2”).

## Ange – 3NF, BCNF & assumptions review

1. Read sections **1.8 Assumptions**, **Stage 3** and **Stage 4** of the document.
2. For each of the 5 assumptions, decide: agree, or disagree and why. Pay most attention to
   assumption 1 (a worker and a supplier on the same row are not related). If you disagree, tell
   Tito, because it changes the design.
3. Open `3NF/projects.csv`, `clients.csv` and `supervisors.csv`. Confirm that joining them on
   ClientID and SupervisorID gives back the same data as `2NF/projects.csv`.
4. Check the 4 counterexamples in the BCNF table against the CSV files (e.g. find P004’s two
   Glass Panels suppliers in `project_material_supply.csv`).
5. **Send back:** a short review note (agree/disagree for each assumption + anything wrong you found).
6. **Presentation:** explain 3NF and BCNF, including why BCNF needed no split.

## Christian – 4NF check & ER diagram

1. Check the 4NF files against the raw data:
   - `worker_skills.csv`: every skill each worker has on any row appears exactly once
   - `supplier_phones.csv`: every phone appears once, with the right supplier
   - `project_workers.csv`: 15 rows, one per raw row
2. Draw the ER diagram of the final design (the 11 files in `4NF/`) using
   [dbdiagram.io](https://dbdiagram.io) or [draw.io](https://app.diagrams.net). Show each table, its
   primary key, and every foreign key arrow (the list is in the document under “Primary and Foreign
   Key Summary”).
3. **Send back:** the diagram as a PNG. It replaces the text diagram in the document.
4. **Presentation:** explain 4NF and walk through the final diagram.

---

## How we finish

1. Everyone sends their result to Tito.
2. Tito adds them to the document, regenerates the PDF and rebuilds `Group5_Normalization_Submission.zip`.
3. Everyone checks the final PDF once before it is submitted.
