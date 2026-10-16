# Rubric checklist: Stage 1 (1NF) and Stage 2 (2NF)

Each question the assignment asks, where the document answers it, and whether the answer was checked against the data.

## Correct 1NF transformation (15 marks)

| Requirement | Where | Status |
|---|---|---|
| 1NF CSV file(s) submitted | `1NF/construction_1nf.csv` | Done, 280 rows, verified |
| Each cell holds one value | `verify_1nf.py` | Done, no `\|`, no empty or padded cells |
| No repeating groups | Stage 1, "How did we make the values atomic?" | Done |
| Each row uniquely identified | Stage 1, "What key identifies each row?" | Done, key unique (wording fixed, finding 1) |
| Which columns violated 1NF? | Stage 1 | Done, all 7 named |
| How did you make values atomic? | Stage 1 | Done, includes paired material/cost split |
| New rows, new tables, or both? | Stage 1 | Done, "new rows only", with the reason |
| What key identifies each row? | Stage 1 | **Fix needed:** replace the "no smaller set" sentence (finding 1) |
| Don't jump to 3NF/4NF | Stage 1 | Done, single table kept |

## Correct 2NF transformation (15 marks)

| Requirement | Where | Status |
|---|---|---|
| 2NF CSV file(s) submitted | `2NF/` (6 files) | Done, verified against raw and 1NF |
| Which tables had composite keys? | Stage 2 | Done |
| Which columns depended on part of the key? | Stage 2 table | Done, all 5 dependencies hold on every row |
| Which data moved into separate tables? | Stage 2 table | Done, row counts match the files |
| What PKs and FKs were introduced? | Stage 2 | Done, all FKs resolve (0 orphans) |
| Why is the design now in 2NF? | Stage 2 | **Fix needed:** material price sentence (finding 2) |
| Decomposition loses nothing | `verify_2nf.py` | Done, the join rebuilds 1NF exactly |

## Related marks my part supports

| Rubric item | What I checked |
|---|---|
| Identification of raw data problems (10) | Every multi-valued cell and its sizes, row by row (`1nf_row_traces.md`) |
| Correct primary and foreign keys (10) | 1NF key justified by meaning; 2NF PKs unique; FKs resolve; surrogate keys map 1:1 to names |
| Quality of explanation and presentation (5) | Speaker notes and likely questions (`presentation_notes.md`) |

## Result

Both stages are complete and every number in the document checks out. Two sentences have to be replaced
before the final PDF ([findings_and_corrections.md](findings_and_corrections.md)). With those replaced,
Stage 1 and Stage 2 answer every question the assignment asks, and every claim matches the data.
