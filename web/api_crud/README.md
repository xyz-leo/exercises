# Flask REST API - To-Do Tasks

A simple Flask RESTful API for managing to-do tasks using SQLite and SQLAlchemy.

## Features

- Create tasks
- List all tasks
- Retrieve a single task by ID
- Update tasks
- Delete tasks

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy

## Setup

1. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:

```bash
pip install Flask Flask-SQLAlchemy
```

3. Run the application:

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### GET /tasks
Returns all tasks.

### GET /tasks/<id>
Returns a single task by ID.

### POST /tasks
Create a new task.

Request body:

```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

### PUT /tasks/<id>
Update a task.

Request body:

```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

### DELETE /tasks/<id>
Delete a task.

## Notes

- The database used is `SQLite` and will be created automatically as `tasks.db`.
- You can test the endpoints using curl or a REST client like Postman.

