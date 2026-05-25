# CLI Todo Manager

A simple command-line todo app built with Python. Zero dependencies.

## Project structure

- `todo.py` — main application
- `tasks.json` — data file (auto-created)

## Running

```bash
python todo.py <command>
```

## Key commands

| Command | Alias | Description |
|---------|-------|-------------|
| `add` | `a` | Add task (`-p` priority, `-d` due date) |
| `list` | `ls` | List tasks (`-s` status, `-p` priority, `--search`) |
| `done` | `do` | Mark task done |
| `undo` | `un` | Undo completed task |
| `delete` | `rm`, `del` | Delete task |
| `search` | `find` | Search by keyword |
| `stats` | `st` | Show statistics |
| `clean` | | Remove completed tasks |
