from flask import Blueprint, request
from sqlalchemy.orm import declarative_base
from models import Note
from database import db
from helpers import (
        make_response,
        error_response,
        get_note_or_404,
        validate_json_fields,
        serialize_note,
        serialize_notes
        )

bp = Blueprint('notes', __name__)

@bp.route("/notes", methods=["GET"])
def get_all_notes():
    notes = Note.query.all()
    return make_response(data=serialize_notes(notes), message="All notes retrieved")


@bp.route("/notes/<int:note_id>", methods=["GET"])
def get_one_note(note_id):
    note = get_note_or_404(note_id, Note)
    if isinstance(note, tuple): return note
    return make_response(data=serialize_note(note), message="Note retrieved")


@bp.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    validation = validate_json_fields(data, ["title"])
    if validation: return validation

    note = Note(title=data["title"], content=data.get("content"))
    db.session.add(note)
    db.session.commit()
    return make_response(data={"id": note.id}, message="Note created", status=201)


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


@bp.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = get_note_or_404(note_id, Note)
    if isinstance(note, tuple): return note

    db.session.delete(note)
    db.session.commit()
    return make_response(message="Note deleted")
