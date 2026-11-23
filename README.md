# Task Tracker

A small Python command-line task tracker. It stores tasks in `tasks.json` in the current working directory.

## Requirements and setup

- Python 3.12 (the supplied historical logs were produced on Linux with Python 3.13.18).
- Install the pinned test dependency:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Commands

Run from this directory:

```bash
python -m tasktracker.cli add "Write report" --priority high --due 2026-12-01
python -m tasktracker.cli list --status pending --sort priority
python -m tasktracker.cli done 1
python -m tasktracker.cli delete 1
python -m tasktracker.cli summary
```

Priorities are `high`, `medium`, and `low`. Due dates must be real calendar dates in `YYYY-MM-DD` format or omitted.

## Tests

```bash
pytest -v
```

The archive includes historical baseline and post-fix logs in `logs/`. Those logs were generated on Linux/Python 3.13.18, not on the submitter's Windows/Python 3.12 machine. Re-run tests locally and retain the actual output/screenshot for submission. Do not present the included logs as proof of a Windows/Python 3.12 run.

## Current limitations

- `tasks.json` is resolved relative to the current working directory; there is no `--file` option.
- Invalid/corrupted JSON is not handled with a user-friendly recovery path.
- Writes are not atomic and there is no file locking.
- Storage has no dedicated tests; CLI coverage is limited.
- No CI, lint, type-check, or build configuration is included.
- The CLI has no `export` command; do not rely on one.

See `TASKS_01_10_AND_EVIDENCE.md` for the audit, acceptance criteria, risk register, mitigation records, readiness review, AI-use record, and evidence appendix.
