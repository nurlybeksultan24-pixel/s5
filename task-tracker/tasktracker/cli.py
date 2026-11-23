"""Command line interface."""
import argparse
from tasktracker import storage
from tasktracker.tracker import TaskTracker


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tasktracker")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add")
    p_add.add_argument("title")
    p_add.add_argument("--priority", default="medium")
    p_add.add_argument("--due", default=None)

    p_list = sub.add_parser("list")
    p_list.add_argument("--status", default="all")
    p_list.add_argument("--sort", default=None)

    p_done = sub.add_parser("done")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("delete")
    p_del.add_argument("id", type=int)

    sub.add_parser("summary")

    args = parser.parse_args(argv)
    tracker = TaskTracker(storage.load())

    if args.cmd == "add":
        t = tracker.add(args.title, args.priority, args.due)
        storage.save(tracker.tasks)
        print(f"Added #{t['id']}: {t['title']}")
    elif args.cmd == "list":
        for t in tracker.list(args.status, args.sort):
            mark = "x" if t["done"] else " "
            due = t["due"] if t["due"] else "-"
            print(f"[{mark}] #{t['id']} {t['title']} ({t['priority']}, due {due})")
    elif args.cmd == "done":
        t = tracker.complete(args.id)
        if t:
            storage.save(tracker.tasks)
            print(f"Completed #{t['id']}")
        else:
            print("Task not found")
    elif args.cmd == "delete":
        tracker.delete(args.id)
        storage.save(tracker.tasks)
        print(f"Deleted #{args.id}")
    elif args.cmd == "summary":
        s = tracker.summary()
        print(f"Total: {s['total']}, Done: {s['done']}, Pending: {s['pending']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
