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


def _sample():
    t = TaskTracker()
    t.add("banana", "low", "2026-12-02")
    t.add("Apple", "high", None)
    t.add("cherry", "medium", "2026-12-01")
    return t


def test_sort_by_priority():
    assert [x["title"] for x in _sample().list(sort_by="priority")] == ["Apple", "cherry", "banana"]


def test_sort_by_due_none_last():
    assert [x["title"] for x in _sample().list(sort_by="due")] == ["cherry", "banana", "Apple"]


def test_sort_by_title_case_insensitive():
    assert [x["title"] for x in _sample().list(sort_by="title")] == ["Apple", "banana", "cherry"]


def test_filter_done():
    t = _sample()
    t.complete(1)
    assert [x["title"] for x in t.list("done")] == ["banana"]


def test_unknown_sort_keeps_insertion_order():
    assert [x["title"] for x in _sample().list(sort_by="foo")] == ["banana", "Apple", "cherry"]


# --- Task 07: regression tests for risks F1 and F2 ---
import pytest


def test_id_not_reused_after_delete():
    t = TaskTracker()
    t.add("A")
    t.add("B")
    t.delete(1)
    c = t.add("C")
    assert c["id"] == 3
    assert len({x["id"] for x in t.tasks}) == len(t.tasks)


def test_complete_targets_correct_task_after_delete():
    t = TaskTracker()
    t.add("A")
    t.add("B")
    t.delete(1)
    t.add("C")
    t.complete(3)
    assert [(x["title"], x["done"]) for x in t.tasks] == [("B", False), ("C", True)]


def test_invalid_priority_rejected():
    with pytest.raises(ValueError):
        TaskTracker().add("A", "urgent")


@pytest.mark.parametrize("bad", ["tomorrow", "2026-13-01", "2026-02-30", "01-12-2026", ""])
def test_invalid_due_rejected(bad):
    with pytest.raises(ValueError):
        TaskTracker().add("A", due=bad)


def test_rejected_task_is_not_stored():
    t = TaskTracker()
    with pytest.raises(ValueError):
        t.add("A", "urgent")
    assert t.tasks == []


def test_valid_due_and_none_accepted():
    t = TaskTracker()
    assert t.add("A", due="2026-12-01")["due"] == "2026-12-01"
    assert t.add("B", due=None)["due"] is None


def test_cli_rejects_invalid_priority(tmp_path, monkeypatch, capsys):
    from tasktracker import cli
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as e:
        cli.main(["add", "A", "--priority", "urgent"])
    assert e.value.code != 0
    assert "priority" in capsys.readouterr().err
    assert not (tmp_path / "tasks.json").exists()
