"""JSON file storage."""
import json
import os

DATA_FILE = "tasks.json"


def load(path=DATA_FILE):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def save(tasks, path=DATA_FILE):
    with open(path, "w") as f:
        json.dump(tasks, f)
