import json
import argparse
from datetime import datetime
from pathlib import Path

TASK_FILE = Path("tasks.json")


def load_tasks():
    if TASK_FILE.exists():
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def generate_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1


def add_task(args):
    tasks = load_tasks()
    task = {
        "id": generate_id(tasks),
        "title": args.title,
        "description": args.description or "",
        "priority": args.priority,
        "due_date": args.due,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added with ID {task['id']}")


def list_tasks(args):
    tasks = load_tasks()

    if args.status:
        tasks = [t for t in tasks if t["status"] == args.status]

    if args.priority:
        tasks = [t for t in tasks if t["priority"] == args.priority]

    if args.sort == "due":
        tasks.sort(key=lambda x: x["due_date"] or "")
    elif args.sort == "priority":
        priority_order = {"low": 1, "medium": 2, "high": 3}
        tasks.sort(key=lambda x: priority_order[x["priority"]], reverse=True)

    if not tasks:
        print("No tasks found.")
        return

    for t in tasks:
        print(
            f"[{t['id']}] {t['title']} | "
            f"Priority: {t['priority']} | "
            f"Status: {t['status']} | "
            f"Due: {t['due_date'] or 'N/A'}"
        )


def mark_done(args):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.id:
            task["status"] = "completed"
            save_tasks(tasks)
            print("Task marked as completed.")
            return
    print("Task not found.")


def delete_task(args):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != args.id]
    if len(new_tasks) == len(tasks):
        print("Task not found.")
        return
    save_tasks(new_tasks)
    print("Task deleted.")


def main():
    parser = argparse.ArgumentParser(description="CLI Task Manager")
    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")
    add_parser.add_argument("-d", "--description")
    add_parser.add_argument("-p", "--priority", choices=["low", "medium", "high"], default="medium")
    add_parser.add_argument("--due", help="Due date YYYY-MM-DD")
    add_parser.set_defaults(func=add_task)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", choices=["pending", "completed"])
    list_parser.add_argument("--priority", choices=["low", "medium", "high"])
    list_parser.add_argument("--sort", choices=["due", "priority"])
    list_parser.set_defaults(func=list_tasks)

    done_parser = subparsers.add_parser("done")
    done_parser.add_argument("id", type=int)
    done_parser.set_defaults(func=mark_done)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)
    delete_parser.set_defaults(func=delete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
 
 