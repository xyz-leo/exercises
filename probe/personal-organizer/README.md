# Personal Organizer

Personal Organizer is a minimalistic task management application built with Python and PySide6. It allows users to create and switch between multiple workspaces, each containing its own list of tasks. The application stores data locally using SQLite and is designed to be lightweight and simple to use.

## Features
- Multiple workspaces for task separation
- Add, view, complete, and delete tasks
- SQLite database for persistent local storage
- Automatically switches to a new workspace upon creation
- Remove workspaces safely with confirmation
- Custom icon and clean user interface
- Ready for packaging as a standalone executable

## Requirements
- Python 3.11 or higher
- PySide6

## Installation
Install dependencies with:
```bash
pip install -r requirements.txt
```

## Building with PyInstaller
- Use the following command to build a standalone executable on Windows:
``` Terminal
pyinstaller --onefile --icon=".files\icon.ico" organizer.py --clean --noconsole
```
