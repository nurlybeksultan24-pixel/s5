# Task Tracker

A small command-line task tracker written in Python. Tasks are stored in `tasks.json`.

## Requirements
- Python 3.8+
- pytest (for tests)

## Usage
```
python -m tasktracker.cli add "Write report" --priority high --due 2026-12-01
python -m tasktracker.cli list --status pending --sort priority
python -m tasktracker.cli done 1
python -m tasktracker.cli delete 1
python -m tasktracker.cli summary
```

## Features
- Add, complete, delete tasks
- Priorities: high, medium, low
- Filter by status, sort by priority/due/title
- Tasks are validated before saving
- Export tasks to CSV with `export` command

## Tests
```
pytest
```
