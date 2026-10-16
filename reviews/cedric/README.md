# Cedric: 1NF and 2NF verification

My part of [TEAM_TASKS.md](../../TEAM_TASKS.md): check the 1NF and 2NF files against the raw data,
send the results to Tito and present Stage 1 and Stage 2.

## Files

| File | What it is |
|---|---|
| [1nf_row_traces.md](1nf_row_traces.md) | Raw rows 1, 9 and 15 traced into the 1NF file, plus the row-count table for all 15 |
| [2nf_checks.md](2nf_checks.md) | Duplicates, keys, values, foreign keys and the lossless join for the 2NF tables |
| [findings_and_corrections.md](findings_and_corrections.md) | Two sentences in the document that are wrong, with replacement text |
| [send_back_summary.md](send_back_summary.md) | The 3–5 sentences for Tito to paste into the document |
| [presentation_notes.md](presentation_notes.md) | What to say for Stage 1 and Stage 2, with likely questions |
| [rubric_checklist.md](rubric_checklist.md) | Every 1NF/2NF rubric question and where it is answered |

## Run the checks

From the project root (Python 3.10+, no packages needed):

```sh
python3 scripts/verify_1nf.py
python3 scripts/verify_2nf.py
python3 scripts/verify_1nf_key.py
```

Each script prints PASS/FAIL per check and exits with code 1 if anything fails. `[NOTE]` lines are
observations, not failures. They are explained in [findings_and_corrections.md](findings_and_corrections.md).

These files are for the team and are not part of the zip. `scripts/make_zip.sh` only packages the stage
folders and the explanation document.
