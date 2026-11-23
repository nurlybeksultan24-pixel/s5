# AGENTS.md

## Purpose and scope
This repository is a small local Python CLI task tracker. Data is stored in `tasks.json` in the current working directory. Keep work limited to this repository.

## Repository map
- `tasktracker/cli.py`: argparse entry point and command dispatch (`main`).
- `tasktracker/tracker.py`: `TaskTracker` business logic, validation, filtering, sorting, summary.
- `tasktracker/storage.py`: JSON persistence (`load`, `save`).
- `tests/test_tracker.py`: unit and regression tests.
- `requirements.txt`: pinned test dependency.
- `README.md`: setup, usage, limitations.
- `TASKS_01_10_AND_EVIDENCE.md`: assignment audit and evidence notes.
- `logs/`: historical test logs and diffs.

## Setup
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Allowed / safe commands
- Read repository files and inspect `git status`, `git diff`, `git log`.
- `python --version`, `python -m pip --version`.
- `pytest -v` (and focused pytest node IDs).
- Run non-destructive CLI read commands such as `python -m tasktracker.cli list` and `summary`.
- `python -m compileall -q tasktracker tests` for syntax compilation.
- `ruff check` or `mypy` only after the relevant tool is installed and approved.

## Ask for human approval first
- Install, remove, or upgrade packages; edit `requirements.txt`.
- Change the JSON data format or delete/overwrite user task data.
- Add/remove files outside the documented task scope.
- Create commits, push, merge, deploy, or publish.
- Run network-dependent commands or commands with broad filesystem effects.

## Forbidden
- Read, print, create, or transmit secrets, tokens, credentials, or `.env` contents.
- Production deployment or package publishing.
- Destructive commands such as `rm -rf`, `Remove-Item -Recurse`, `git reset --hard`, or `git push --force`.
- Unreviewed dependency changes.
- Access or modify files outside this repository.
- Network access unless explicitly approved.

## Coding and safety conventions
- Target Python 3.12; use 4-space indentation and standard-library code unless approved otherwise.
- Keep business logic in `tracker.py`; keep terminal I/O in `cli.py`.
- Make small, focused changes. Do not edit tests merely to make a change pass.
- Preserve task data. Never use real personal or confidential data in test fixtures.
- Treat JSON input as untrusted; validate before persisting.

## Test and review expectations
- Run `pytest -v` before and after a code change when feasible.
- Add regression coverage for changed behavior.
- Report exact command, environment, output, and anything not tested.
- Show the complete diff and wait for human approval before committing or applying risky changes.
- Never claim a test/build/lint/type-check passed unless it was actually run.

## Agent instruction loading
For this submission, `AGENTS.md` was manually opened/read by the human/assistant during the review. There is no evidence that Claude automatically discovered or loaded it. Therefore automatic instruction loading is **not verified**; do not claim that it occurred.
