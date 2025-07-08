# Notes API – Flask CRUD with Helpers

This project implements a clean and minimal RESTful API using Flask + SQLAlchemy + SQLite. It includes full CRUD operations and helper functions to ensure code reusability, clarity, and maintainability.

---

## Code Block Explanations

---

### Blueprint Declaration (`routes.py`)

```python
bp = Blueprint('notes', __name__)
```

Defines a Blueprint named `notes`. Blueprints allow you to organize routes into modular components and register them later in the main application using `app.register_blueprint()`.

---

### Helper: make_response

```python
def make_response(data=None, message="", status=200):
    return jsonify({
        "status": "success" if 200 <= status < 300 else "error",
        "message": message,
        "data": data
    }), status
```

Standardizes all API responses into a consistent structure. It avoids repeating `jsonify()` in every route and ensures every response contains a `status`, `message`, and `data` field.

---

### Helper: error_response

```python
def error_response(message, status=400):
    return make_response(data=None, message=message, status=status)
```

Shortcut to quickly return an error response using the same structure as `make_response`.

---

### Helper: get_note_or_404

```python
def get_note_or_404(note_id, model):
    note = model.query.get(note_id)
    if not note:
        return error_response("Note not found", status=404)
    return note
```

Retrieves a record from the database. If the record doesn't exist, returns a standardized 404 error response. Otherwise, returns the object.

---

### Helper: validate_json_fields

```python
def validate_json_fields(data, required_fields):
    missing = [field for field in required_fields if field not in data]
    if missing:
        return error_response(f"Missing fields: {', '.join(missing)}", status=400)
    return None
```

Validates whether the required fields are present in a JSON payload. If any are missing, returns a 400 error response listing the missing fields.

---

### Helper: serialize_note

```python
def serialize_note(note):
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat()
    }
```

Converts a SQLAlchemy `Note` object into a plain dictionary suitable for JSON responses.

---

### Helper: serialize_notes

```python
def serialize_notes(notes):
    return [serialize_note(n) for n in notes]
```

Maps a list of `Note` objects into a list of serialized dictionaries using `serialize_note()`.

---

### Route: GET /notes

```python
@bp.route("/notes", methods=["GET"])
def get_all_notes():
    notes = Note.query.all()
    return make_response(data=serialize_notes(notes), message="All notes retrieved")
```

Retrieves all notes from the database, serializes them, and returns them in a consistent format.

---

### Route: GET /notes/<note_id>

```python
@bp.route("/notes/<int:note_id>", methods=["GET"])
def get_one_note(note_id):
    note = get_note_or_404(note_id, Note)
    if isinstance(note, tuple): return note
    return make_response(data=serialize_note(note), message="Note retrieved")
```

Retrieves a specific note by its ID. If not found, returns a 404 error.

---

### Route: POST /notes

```python
@bp.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    validation = validate_json_fields(data, ["title"])
    if validation: return validation

    note = Note(title=data["title"], content=data.get("content"))
    db.session.add(note)
    db.session.commit()
    return make_response(data={"id": note.id}, message="Note created", status=201)
```

Creates a new note. Validates the presence of the `title` field. Responds with the new note’s ID upon success.

---

### Route: PUT /notes/<note_id>

```python
@bp.route("/notes/<int:note_id>", methods=["PUT"])
def replace_note(note_id):
    note = get_note_or_404(note_id, Note)
    if isinstance(note, tuple): return note

    data = request.get_json()
    validation = validate_json_fields(data, ["title"])
    if validation: return validation

    note.title = data["title"]
    note.content = data.get("content")
    db.session.commit()
    return make_response(message="Note replaced")
```

Replaces all fields of an existing note. Requires the `title` field to be present.

---

### Route: PATCH /notes/<note_id>

```python
@bp.route("/notes/<int:note_id>", methods=["PATCH"])
def update_note(note_id):
    note = get_note_or_404(note_id, Note)
    if isinstance(note, tuple): return note

    data = request.get_json()
    if "title" in data:
        note.title = data["title"]
    if "content" in data:
        note.content = data["content"]
    db.session.commit()
    return make_response(message="Note updated")
```

Partially updates a note. Only the fields included in the request body will be modified.

---

### Route: DELETE /notes/<note_id>

```python
@bp.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = get_note_or_404(note_id, Note)
    if isinstance(note, tuple): return note

    db.session.delete(note)
    db.session.commit()
    return make_response(message="Note deleted")
```

Deletes a note by its ID. Returns a success message upon deletion.

## API Testing Script (`test_api.sh`)

This project includes a shell script named `test_api.sh`, which automates HTTP requests to the API using `curl`. It simulates a complete sequence of CRUD operations (Create, Read, Update, Delete) on the `Note` entity.

The purpose of this script is to simplify manual testing during development. It allows you to verify whether all routes are working correctly and whether the data is being processed as expected. It also saves time by eliminating the need to use tools like Postman or manually run commands for each endpoint.

### How the script works

The script performs the following steps in order:

1. **POST** – Creates a new note with a title and optional content.
2. **GET (all)** – Retrieves all notes from the database.
3. **GET (one)** – Retrieves a specific note by ID.
4. **PUT** – Replaces all fields of the note.
5. **PATCH** – Updates only the provided fields of the note.
6. **GET (one)** – Retrieves the updated note.
7. **DELETE** – Deletes the note by ID.
8. **GET (one)** – Confirms that the note was deleted by attempting to retrieve it again.

### Usage

Make sure your Flask app is running (default: `http://localhost:5000`). Then run:

```bash
chmod +x test_api.sh
./test_api.sh
```

You can modify the base URL inside the script if your server is running on a different port or environment.

## Manual API Testing with `curl`

Below are example `curl` commands for manually testing each route of the Notes API. Make sure your Flask server is running at `http://localhost:5000`.

All requests assume the resource path is `/notes`.

---

### 1. Create a new note (POST)

```bash
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "content": "Write clean APIs"}'
```

---

### 2. Get all notes (GET)

```bash
curl http://localhost:5000/notes
```

---

### 3. Get a specific note by ID (GET)

```bash
curl http://localhost:5000/notes/1
```

---

### 4. Replace a note completely (PUT)

```bash
curl -X PUT http://localhost:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title", "content": "Completely replaced content"}'
```

---

### 5. Update part of a note (PATCH)

```bash
curl -X PATCH http://localhost:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated only the content"}'
```

---

### 6. Delete a note (DELETE)

```bash
curl -X DELETE http://localhost:5000/notes/1
```

---

### 7. Confirm deletion (GET)

```bash
curl http://localhost:5000/notes/1
```

If the note has been deleted, the response should include `"status": "error"` and a 404 message.

