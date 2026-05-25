# CLI Todo Manager

A simple command-line todo app built with Python. Zero Python dependencies.

## Project structure

- `todo.py` — main application
- `audio_convert.py` — audio converter plugin (requires `ffmpeg` on PATH)
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
| `audio` | `au` | Audio converter plugin (see below) |

## Audio plugin

Convert 50+ audio formats to WAV/MP3. Requires ffmpeg.

```bash
python todo.py audio formats          # List supported input formats
python todo.py audio convert <path>   # Convert files/directories
```

### Convert options

| Flag | Description |
|------|-------------|
| `--to wav\|mp3\|both` | Output format (default: both) |
| `-o, --outdir DIR` | Output directory (default: ./converted) |
| `--mp3-bitrate 320k` | MP3 quality: 128k, 192k, 256k, 320k |
| `--wav-bit 16\|24` | WAV bit depth |
| `-r, --samplerate N` | Resample audio |
| `-R, --recursive` | Recurse into directories |
| `--delete-original` | Delete source after conversion |

### Examples

```bash
python todo.py audio convert song.flac --to mp3
python todo.py audio convert music/ -R --to both -o output/
python audio_convert.py             # standalone mode also works
```
