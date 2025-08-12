# Offline Task Manager (HTML + CSS + JS Only)

This is a fully offline, self-contained Task Manager application built with only HTML, CSS, and JavaScript. No server or backend is required — all data is stored in the browser using `localStorage`.

> Disclaimer: This application is entirely client-side. No encryption or server-side processing is involved. All data is stored in the browser's localStorage. It is recommended for personal, non-sensitive use only.

The primary goal in creating this web application was to build a task manager (to-do list) that is simple, lightweight, useful, and practical for everyday use, allowing users to save and import tasks easily without needing to install or configure anything, or run a server. Just opening the .html file in a browser will work — it runs great on both smartphones and desktop devices.

## Screenshot

<img width="613" height="882" alt="offlinetaskmanager_screenshot" src="https://github.com/user-attachments/assets/e135d8a5-1987-4899-864f-703e07965170" />

## Features

- Add tasks with a title and optional description
- Mark tasks as done or not done
- Delete individual tasks
- Automatically saves tasks locally in the browser
- Set a simple password on first access (stored locally)
- Export tasks as a `.json` file
- Import `.json` files to restore or merge tasks
- Responsive design with minimal styling

## How it Works

- Tasks are stored as an array of objects in `localStorage`, under the key `todo-tasks`
- The password (if set) is stored in plain text in `localStorage` under the key `todo-password`
- Importing a `.json` file merges tasks with the existing ones
- Exported files contain the full list of tasks in JSON format

## How to Use

1. Open the `taskManager.html` file in your browser (If it was downloaded with a .txt extension, simply rename it to .html before opening.)
2. Set a password on first access (required to proceed)
3. Add tasks using the form
4. Use the buttons to export or import `.json` backups
5. All changes are saved automatically

## Data Format

Each task in the JSON array has the following structure:

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "done": false
}
```

## Limitations

- Data is limited to approximately 5MB (browser `localStorage` limit)
- All data is stored locally and unencrypted
- If browser data is cleared, all tasks will be lost unless exported


## Why This Project Matters
The development approach strictly followed the KISS principle, prioritizing simplicity, speed, and ease of use over unnecessary complexity or dependencies.

While this project may appear simple at first glance, its design solves a very real and common problem: the lack of lightweight, truly offline task management tools that require zero setup or installation.

In an era dominated by cloud-based apps, heavy frameworks, and backend dependencies, this project demonstrates that it's still possible — and sometimes preferable — to solve a problem with pure HTML, CSS, and JavaScript. No server, no database, no login — just open the file and use it instantly.

This application reflects a key principle in software engineering:

    Solve the problem in the simplest way possible, without over-engineering.

It also shows attention to:

    User experience: instant access, smooth interactions, no distractions

    Portability: can run on any modern browser, including mobile

    Resilience: data stays on the user's machine, with export/import options

    Practicality: tasks are preserved even offline, and no external services are required

The goal was never to build something complex — it was to build something that works, efficiently and reliably, with zero friction. This project demonstrates thoughtful design, intentional simplicity, and real-world usability — values that matter in real development environments.


## License

This project is free to use and modify for personal or educational purposes.
