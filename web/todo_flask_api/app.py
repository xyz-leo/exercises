# app.py

from flask import Flask, render_template
from database import db
from routes import bp as tasks_bp
import os

# Create Flask app instance
# Explicitly specify template folder path (optional, default is 'templates')
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# Configure SQLAlchemy database URI (SQLite local file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

# Disable track modifications to avoid overhead warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with this Flask app context
db.init_app(app)

# Register the tasks blueprint for routes under '/tasks'
app.register_blueprint(tasks_bp)

# Route to serve the frontend HTML page (index.html)
@app.route("/")
def serve_frontend():
    return render_template("index.html")  # Render from 'templates/index.html'

# Run app with debug mode on if script is run directly
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # Create tables if they do not exist yet
    app.run(debug=True)
