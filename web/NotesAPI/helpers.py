from flask import jsonify

def make_response(data=None, message="", status=200):
    return jsonify({
        "status": "success" if 200 <= status < 300 else "error",
        "message": message,
        "data": data
        }), status


def get_note_or_404(note_id, model):
    note = model.query.get(note_id)
    if not note:
        return make_response(message="Note not found", status=404)
    return note


def serialize_note(note):
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat()
    }


def serialize_notes(notes):
    return [serialize_note(n) for n in notes]


def validate_json_fields(data, required_fields):
    missing = [field for field in required_fields if field not in data]
    if missing:
        return make_response(message=f"Missing fields: {', '.join(missing)}", status=400)
    return None


def error_response(message, status=400):
    return make_response(data=None, message=message, status=status)
