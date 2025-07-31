# Task Manager API with Flask

<img width="960" height="774" alt="Captura de tela 2025-07-31 204344" src="https://github.com/user-attachments/assets/0c4a3a31-77ca-486b-bcc4-1c19d745021e" />

This is a simple Task Manager project built with Flask and SQLite. It provides a RESTful API and a frontend interface to create, read, update, and delete tasks.

## Features

- Create, read, update (replace and partial), and delete tasks via API endpoints
- Frontend interface to interact with the API using HTML, CSS, and JavaScript
- Tasks have title, optional description, and creation timestamp
- Uses Flask Blueprints and SQLAlchemy ORM

## Project Structure

```
.
├── app.py              # Main Flask application
├── database.py         # Database setup and initialization
├── helpers.py          # Helper functions for responses and validation
├── models.py           # SQLAlchemy models (Task)
├── routes.py           # API route definitions using Blueprint
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css       # CSS stylesheet for frontend
└── templates/
    └── index.html      # Frontend HTML page
```

## Setup Instructions

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and go to:

```
http://localhost:5000/
```

## API Endpoints

| Method | Endpoint         | Description                   |
|--------|------------------|-------------------------------|
| GET    | `/tasks/`        | Retrieve all tasks             |
| POST   | `/tasks/`        | Create a new task              |
| GET    | `/tasks/<id>`    | Get a task by ID               |
| PUT    | `/tasks/<id>`    | Replace a task by ID           |
| PATCH  | `/tasks/<id>`    | Partially update a task by ID  |
| DELETE | `/tasks/<id>`    | Delete a task by ID            |

## Notes

- The frontend uses JavaScript `fetch` API to communicate with the backend API.
- Task creation requires at least a `title`.
- `created_at` is automatically set when the task is created.
- The project uses SQLite as the database, stored in `instance/tasks.db`.

## License

This project is for practice purposes.
