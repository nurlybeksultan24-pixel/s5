"""Core task logic."""
from datetime import datetime

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

VALID_PRIORITIES = tuple(PRIORITY_ORDER)

STATUS_FILTERS = {
    "done": lambda t: t["done"],
    "pending": lambda t: not t["done"],
}

SORT_KEYS = {
    "priority": lambda t: PRIORITY_ORDER[t["priority"]],
    "due": lambda t: t["due"] or "9999-12-31",
    "title": lambda t: t["title"].lower(),
}


def _validate_due(due):
    """Accept None or a real calendar date written as YYYY-MM-DD."""
    if due is None:
        return
    try:
        ok = datetime.strptime(due, "%Y-%m-%d").strftime("%Y-%m-%d") == due
    except (ValueError, TypeError):
        ok = False
    if not ok:
        raise ValueError(f"invalid due date {due!r}: expected YYYY-MM-DD")


class TaskTracker:
    def __init__(self, tasks=None):
        self.tasks = tasks or []

    def add(self, title, priority="medium", due=None):
        if priority not in VALID_PRIORITIES:
            raise ValueError(
                f"invalid priority {priority!r}: expected one of {', '.join(VALID_PRIORITIES)}"
            )
        _validate_due(due)
        next_id = max((t["id"] for t in self.tasks), default=0) + 1
        task = {
            "id": next_id,
            "title": title,
            "priority": priority,
            "due": due,
            "done": False,
        }
        self.tasks.append(task)
        return task

    def complete(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["done"] = True
                return t
        return None

    def delete(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]

    def list(self, status="all", sort_by=None):
        keep = STATUS_FILTERS.get(status)
        result = [t for t in self.tasks if keep(t)] if keep else list(self.tasks)
        key = SORT_KEYS.get(sort_by)
        if key:
            result.sort(key=key)
        return result

    def summary(self):
        total = len(self.tasks)
        done = len([t for t in self.tasks if t["done"]])
        return {"total": total, "done": done, "pending": total - done}
