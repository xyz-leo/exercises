# Import the necessary libraries from Flask and SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the Flask application
app = Flask(__name__)

# Configure the database URI (SQLite file named 'tasks.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

# Disable a feature that unnecessarily tracks modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the database object
db = SQLAlchemy(app)

# Define the Task model (represents the 'tasks' table)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)                    # Unique task ID
    title = db.Column(db.String(100), nullable=False)               # Task title (required)
    description = db.Column(db.Text)                                # Task description (optional)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)    # Automatically set creation time

# Route for creating a task (POST) or listing all tasks (GET)
@app.route("/tasks", methods=["GET", "POST"])
def handle_tasks():
    # If the method is POST, create a new task
    if request.method == "POST":
        data = request.get_json()                                   # Get JSON data from request body

        title = data.get("title")                                   # Extract 'title' field
        description = data.get("description")                       # Extract 'description' field

        if not title:
            return jsonify({"error": "Title is required"}), 400     # Return 400 if title is missing

        # Create a new Task object
        new_task = Task(title=title, description=description)
        db.session.add(new_task)                                    # Add task to the session
        db.session.commit()                                         # Commit (save) changes to database

        # Return a JSON response with the new task
        return jsonify({
            "message": "Task created",
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "created_at": new_task.created_at.isoformat()
            }
        }), 201

    # If the method is GET, return all tasks
    else:
        tasks = Task.query.order_by(Task.created_at.desc()).all()   # Get all tasks ordered by date
        result = []

        # Convert each Task object to a dictionary
        for task in tasks:
            result.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "created_at": task.created_at.isoformat()
            })

        return jsonify(result)                                      # Return the list as JSON

# get a specific task
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "created_at": task.created_at.isoformat()
    })


# Route to update an existing task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()                                       # Get JSON data from client

    task = Task.query.get(id)                                       # Find task by ID
    if not task:
        return jsonify({'error': 'Task not found'}), 404            # Return 404 if not found

    if 'title' in data:
        task.title = data['title']                                  # Update title
    if 'description' in data:
        task.description = data['description']                      # Update description

    db.session.commit()                                             # Save changes to database

    # Return updated task
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "created_at": task.created_at.isoformat()
    })

# Route to delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)                                       # Find task by ID
    if not task:
        return jsonify({'error': 'Task not found'}), 404            # Return 404 if not found

    db.session.delete(task)                                         # Delete task
    db.session.commit()                                             # Save changes to database

    return jsonify({'message': f'Task {id} deleted'})              # Return confirmation

# Start the server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()                                             # Create tables (only if not exist)
    app.run(debug=True)                                             # Run the app with debug mode on
