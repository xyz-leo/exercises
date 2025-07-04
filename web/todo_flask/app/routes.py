# Routes and CRUD logic
from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Task

bp = Blueprint("main", __name__, template_folder="../templates")

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        if title:
            new_task = Task(title=title, description=description)
            db.session.add(new_task)
            db.session.commit()

        return redirect(url_for("main.index"))
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("index.html", tasks=tasks)

@bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        if not title:
            return "Title is required", 400

        task.title = title
        task.description = description
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("edit.html", task=task)
