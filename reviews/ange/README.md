# Ange: 3NF, BCNF and assumptions review

My part of [TEAM_TASKS.md](../../TEAM_TASKS.md): check Stage 3 and Stage 4, review the five assumptions
in section 1.8, send the results to Tito and present 3NF and BCNF.

## Files

| File | What it is |
|---|---|
| [3nf_checks.md](3nf_checks.md) | The join test (3NF back to 2NF), keys, foreign keys and unchanged tables |
| [bcnf_checks.md](bcnf_checks.md) | The four counterexamples, the BCNF folder check and a brute-force scan for coincidental dependencies |
| [assumptions_review.md](assumptions_review.md) | Agree or disagree for each of the five assumptions, with evidence |
| [send_back_summary.md](send_back_summary.md) | The short note for Tito to paste into the document |
| [presentation_notes.md](presentation_notes.md) | What to say for Stage 3 and Stage 4, with likely questions |

## Run the checks

From the project root (Python 3.10+, no packages needed):

```sh
python3 scripts/verify_3nf_bcnf.py
```

It prints PASS/FAIL per check and exits with code 1 if anything fails. `[NOTE]` lines are observations,
not failures. They are explained in [bcnf_checks.md](bcnf_checks.md).

These files are for the team and are not part of the zip.
