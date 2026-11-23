"""Core task logic."""


class TaskTracker:
    def __init__(self, tasks=None):
        self.tasks = tasks or []

    def add(self, title, priority="medium", due=None):
        task = {
            "id": len(self.tasks) + 1,
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
        if status == "done":
            result = [t for t in self.tasks if t["done"]]
        elif status == "pending":
            result = [t for t in self.tasks if not t["done"]]
        else:
            result = list(self.tasks)

        if sort_by == "priority":
            order = {"high": 0, "medium": 1, "low": 2}
            result.sort(key=lambda t: order[t["priority"]])
        elif sort_by == "due":
            result.sort(key=lambda t: t["due"] or "9999-12-31")
        elif sort_by == "title":
            result.sort(key=lambda t: t["title"].lower())
        return result

    def summary(self):
        total = len(self.tasks)
        done = len([t for t in self.tasks if t["done"]])
        return {"total": total, "done": done, "pending": total - done}
