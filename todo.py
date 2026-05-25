#!/usr/bin/env python3
"""CLI Todo Manager — stores tasks in tasks.json alongside this script."""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

import audio_convert as _plugin_audio

# Fix Unicode output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_FILE = Path(__file__).parent / "tasks.json"

# ── ANSI colors ──────────────────────────────────────────────
C = {
    "reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m",
    "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
    "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
}

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
PRIORITY_COLOR = {"high": C["red"], "medium": C["yellow"], "low": C["dim"]}
STATUS_ICON = {"pending": " ", "done": "x"}


def load():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


# ── Commands ─────────────────────────────────────────────────

def cmd_add(args):
    tasks = load()
    task = {
        "id": next_id(tasks),
        "desc": args.desc,
        "priority": args.priority,
        "due": args.due,
        "status": "pending",
        "created": date.today().isoformat(),
    }
    tasks.append(task)
    save(tasks)
    print(f"{C['green']}✓{C['reset']} Added #{task['id']}: {task['desc']}")


def cmd_list(args):
    tasks = load()
    if getattr(args, "status", None):
        tasks = [t for t in tasks if t["status"] == args.status]
    if getattr(args, "priority", None):
        tasks = [t for t in tasks if t["priority"] == args.priority]
    if getattr(args, "search", None):
        kw = args.search.lower()
        tasks = [t for t in tasks if kw in t["desc"].lower()]

    tasks.sort(key=lambda t: (0 if t["status"] == "pending" else 1, PRIORITY_ORDER.get(t["priority"], 9), t["id"]))

    if not tasks:
        print(f"{C['dim']}No tasks found.{C['reset']}")
        return

    pending = sum(1 for t in tasks if t["status"] == "pending")
    done = sum(1 for t in tasks if t["status"] == "done")
    print(f"\n{C['bold']}Tasks{C['reset']} — {C['yellow']}{pending} pending{C['reset']}, {C['green']}{done} done{C['reset']}\n")

    for t in tasks:
        icon = STATUS_ICON[t["status"]]
        color = C["green"] if t["status"] == "done" else PRIORITY_COLOR.get(t["priority"], C["reset"])
        due_str = f"  {C['dim']}due:{t['due']}{C['reset']}" if t.get("due") else ""
        status_mark = f"{C['green']}[{icon}]{C['reset']}" if t["status"] == "done" else f"{C['dim']}[ ]{C['reset']}"
        print(f"  {status_mark} {color}#{t['id']}{C['reset']} {t['desc']}{due_str}")


def cmd_done(args):
    tasks = load()
    for t in tasks:
        if t["id"] == args.id and t["status"] == "pending":
            t["status"] = "done"
            t["done_at"] = date.today().isoformat()
            save(tasks)
            print(f"{C['green']}✓{C['reset']} Completed #{args.id}: {t['desc']}")
            return
    print(f"{C['red']}✗{C['reset']} Task #{args.id} not found or already done.")


def cmd_undo(args):
    tasks = load()
    for t in tasks:
        if t["id"] == args.id and t["status"] == "done":
            t["status"] = "pending"
            t.pop("done_at", None)
            save(tasks)
            print(f"{C['yellow']}↩{C['reset']} Undone #{args.id}: {t['desc']}")
            return
    print(f"{C['red']}✗{C['reset']} Task #{args.id} not found or not done.")


def cmd_delete(args):
    tasks = load()
    for i, t in enumerate(tasks):
        if t["id"] == args.id:
            removed = tasks.pop(i)
            save(tasks)
            print(f"{C['red']}✗{C['reset']} Deleted #{args.id}: {removed['desc']}")
            return
    print(f"{C['red']}✗{C['reset']} Task #{args.id} not found.")


def cmd_search(args):
    args.status = None
    args.search = args.keyword
    cmd_list(args)


def cmd_clean(args):
    tasks = load()
    done = [t for t in tasks if t["status"] == "done"]
    remaining = [t for t in tasks if t["status"] != "done"]
    save(remaining)
    print(f"{C['green']}✓{C['reset']} Removed {len(done)} completed task(s).")


def cmd_stats(args):
    tasks = load()
    total = len(tasks)
    pending = sum(1 for t in tasks if t["status"] == "pending")
    done = total - pending
    overdue = sum(1 for t in tasks if t["status"] == "pending" and t.get("due") and t["due"] < date.today().isoformat())

    high = sum(1 for t in tasks if t["priority"] == "high" and t["status"] == "pending")

    print(f"\n{C['bold']}Stats{C['reset']}\n")
    print(f"  Total:    {total}")
    print(f"  Pending:  {C['yellow']}{pending}{C['reset']}")
    print(f"  Done:     {C['green']}{done}{C['reset']}")
    print(f"  Overdue:  {C['red']}{overdue}{C['reset']}")
    print(f"  High pri: {C['red']}{high}{C['reset']}")


# ── CLI setup ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="CLI Todo Manager")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", aliases=["a"], help="Add a task")
    p_add.add_argument("desc", help="Task description")
    p_add.add_argument("-p", "--priority", choices=["high", "medium", "low"], default="medium")
    p_add.add_argument("-d", "--due", help="Due date YYYY-MM-DD")

    p_list = sub.add_parser("list", aliases=["ls"], help="List tasks")
    p_list.add_argument("-s", "--status", choices=["pending", "done"])
    p_list.add_argument("-p", "--priority", choices=["high", "medium", "low"])
    p_list.add_argument("--search")

    p_done = sub.add_parser("done", aliases=["do"], help="Mark a task done")
    p_done.add_argument("id", type=int)

    p_undo = sub.add_parser("undo", aliases=["un"], help="Undo a completed task")
    p_undo.add_argument("id", type=int)

    p_del = sub.add_parser("delete", aliases=["rm", "del"], help="Delete a task")
    p_del.add_argument("id", type=int)

    p_search = sub.add_parser("search", aliases=["find"], help="Search tasks by keyword")
    p_search.add_argument("keyword")

    sub.add_parser("clean", help="Remove all completed tasks")
    sub.add_parser("stats", aliases=["st"], help="Show statistics")

    # ── Plugin: audio converter ──
    plugin_handlers = _plugin_audio.register(sub)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    handlers = {
        "add": cmd_add, "a": cmd_add,
        "list": cmd_list, "ls": cmd_list,
        "done": cmd_done, "do": cmd_done,
        "undo": cmd_undo, "un": cmd_undo,
        "delete": cmd_delete, "rm": cmd_delete, "del": cmd_delete,
        "search": cmd_search, "find": cmd_search,
        "clean": cmd_clean,
        "stats": cmd_stats, "st": cmd_stats,
    }

    # Nested subcommand routing (e.g. "audio convert")
    key = (args.command, getattr(args, "audio_cmd", None))
    handler = plugin_handlers.get(key) if key[1] else handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
