from tasktracker.tracker import TaskTracker


def test_add_task():
    t = TaskTracker()
    task = t.add("Write report", "high", "2026-12-01")
    assert task["id"] == 1
    assert task["done"] is False
    assert len(t.tasks) == 1


def test_complete_task():
    t = TaskTracker()
    t.add("A")
    assert t.complete(1)["done"] is True


def test_list_pending():
    t = TaskTracker()
    t.add("A")
    t.add("B")
    t.complete(1)
    assert [x["title"] for x in t.list("pending")] == ["B"]


def test_summary():
    t = TaskTracker()
    t.add("A")
    t.add("B")
    t.complete(2)
    assert t.summary() == {"total": 2, "done": 1, "pending": 1}
