# CLI Todo Manager

A simple command-line todo app built with Python. Zero dependencies.

## Usage

```bash
# Add tasks
python todo.py add "Send weekly report" -p high -d 2026-05-30

# List all tasks
python todo.py ls

# Filter by status and priority
python todo.py ls -s pending -p high

# Search
python todo.py find "report"

# Mark done / undo
python todo.py done 1
python todo.py undo 1

# Delete
python todo.py rm 1

# Stats
python todo.py stats

# Remove all completed tasks
python todo.py clean
```

## Options

| Command | Alias | Description |
|---------|-------|-------------|
| `add` | `a` | Add a task (`-p` priority, `-d` due date) |
| `list` | `ls` | List tasks (`-s` status, `-p` priority, `--search`) |
| `done` | `do` | Mark a task as done |
| `undo` | `un` | Undo a completed task |
| `delete` | `rm`, `del` | Delete a task |
| `search` | `find` | Search by keyword |
| `stats` | `st` | Show statistics |
| `clean` | | Remove all completed tasks |

## Data

Tasks are stored in `tasks.json` in the same directory. Add it to `.gitignore` if you want to keep your tasks private.
