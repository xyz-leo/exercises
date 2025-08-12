# Django Agenda App

This is a **full-stack web application built with Django**, developed for learning and practicing the core concepts of web development using the Django framework.

The project allows authenticated users to manage personal contacts and organize them into categories. Users can create, update, delete, and search for contacts, as well as manage their account information.

> **Important:**\
> This project is **strictly for learning purposes**. It is **not intended for production use**. The code may contain bugs, security flaws, or features that require improvements or refactoring.

---

## Features

- User authentication (register, login, logout, profile update)
- Create, update, delete, and view contacts
- Categorize contacts
- Search functionality (by name, phone, or email)
- Pagination for contacts listing
- Basic responsive layout with custom CSS
- Simple user-friendly interface

---

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** Django Templates, HTML, CSS
- **Database:** SQLite (default Django setup)
- **Authentication:** Django built-in auth system
- **Media handling:** Django's `ImageField` (for contact pictures, but was not used)
- **Deployment:** Local development environment

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/xyz-leo/agenda-django.git
cd agenda-django
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Access the app at:

```
http://127.0.0.1:8000
```

---

## Usage

- Create a user account (Register).
- Login to the system.
- Add, edit, delete, and search for contacts.
- Create categories to organize contacts.
- Update your user information at any time.

---

## Project Structure

```plaintext
├── agenda/               # Django project config
├── contact/               # Main app with models, views, forms
├── base_templates/        # Global templates (base layout, partials)
├── base_static/           # Global static files (CSS)
├── media/                 # Uploaded media (contact pictures)
├── utils/                 # Utility to add fake users script (optional)
├── manage.py
├── requirements.txt
```

---

## Disclaimer

This project was developed purely for **educational purposes** and to practice Django full-stack development.\
It is **not suitable for production use** and may contain errors, security flaws, or incomplete features.

---

## License

This project does not have a license and is intended only for personal learning and experimentation.

