from flask import Blueprint, request
from helpers import *    # Import helper functions like send_response, missing_fields, etc.
from models import Task  # Import the Task model class
from database import db  # Import the SQLAlchemy db instance

# Create a Blueprint named "tasks", all routes here will be prefixed with "/tasks"
bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# POST /tasks/ - Create a new task
@bp.route("/", methods=["POST"])
def create_task():
    data = request.get_json()  # Parse JSON body from request

    # Check if required field 'title' is missing
    missing = missing_fields(req_fields=['title'], data=data)
    if missing:
        # Return 400 Bad Request with message about missing fields
        return send_response(msg=f"Request incomplete. Missing fields: {missing}", status=400, success=False)

    # Create new Task object from data
    task = Task(title=data['title'], description=data.get('description'))

    # Add new task to database session and commit (save)
    db.session.add(task)
    db.session.commit()

    # Return success response with serialized new task and HTTP 201 Created
    return send_response(data=serialize_obj(task), msg="Task created", status=201)


# GET /tasks/ - Retrieve all tasks, ordered by creation date descending
@bp.route("/", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()  # Query all tasks ordered newest first

    # If no tasks found, message will reflect that; else "All tasks retrieved."
    return send_response(
        data=serialize_obj_list(tasks),
        msg="No tasks registered." if not tasks else "All tasks retrieved.",
        status=200
    )


# GET /tasks/<id> - Retrieve a specific task by ID
@bp.route("/<int:id>", methods=["GET"])
def get_task_by_id(id):
    task = find_by_id(model=Task, obj_id=id)  # Fetch task or None if not found

    if not task:
        # If not found, return 404 with error message
        return send_response(msg="Task not found.", status=404, success=False)

    # Return serialized task data with success message
    return send_response(data=serialize_obj(task), msg="Task retrieved", status=200)


# DELETE /tasks/<id> - Delete a specific task by ID
@bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = find_by_id(model=Task, obj_id=id)  # Fetch task or None

    if not task:
        # Return 404 if task not found
        return send_response(msg="Task not found.", status=404, success=False)

    # Delete task from database and commit changes
    db.session.delete(task)
    db.session.commit()

    # Return success response with deleted task data
    return send_response(data=serialize_obj(task), msg="Task deleted successfully.", status=200)


# PUT /tasks/<id> - Replace entire task (full update)
@bp.route("/<int:id>", methods=["PUT"])
def replace_task(id):
    data = request.get_json()  # Parse JSON from request

    # Check required fields, here 'title' must be present for replacement
    missing = missing_fields(req_fields=['title'], data=data)
    if missing:
        # Return 400 if fields missing
        return send_response(msg=f"Request incomplete. Missing fields: {missing}", status=400, success=False)

    task = find_by_id(model=Task, obj_id=id)  # Fetch task to update
    if not task:
        # Return 404 if not found
        return send_response(msg="Task not found.", status=404, success=False)

    # Replace title and description with new data
    task.title = data['title']
    task.description = data.get('description')

    # Commit changes to database
    db.session.commit()

    # Return updated task data with success message
    return send_response(data=serialize_obj(task), msg="Task replaced successfully.", status=200)


# PATCH /tasks/<id> - Partial update to a task (only fields provided will be updated)
@bp.route("/<int:id>", methods=["PATCH"])
def patch_task(id):
    data = request.get_json()  # Parse JSON

    task = find_by_id(model=Task, obj_id=id)  # Fetch task or None
    if not task:
        # 404 if task not found
        return send_response(msg="Task not found.", status=404, success=False)

    # Get fields if present in JSON; can be None if omitted
    title = data.get('title')
    description = data.get('description')

    # Update only fields that are provided (not None)
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    # Commit the partial updates to database
    db.session.commit()

    # Return updated task with success message
    return send_response(data=serialize_obj(task), msg="Task updated successfully.", status=200)
