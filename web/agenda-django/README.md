# Django Agenda App

This is a **full-stack web application built with Django**, developed for learning and practicing the core concepts of web development using the Django framework.

The project allows authenticated users to manage personal contacts and organize them into categories. Users can create, update, delete, and search for contacts, as well as manage their account information.

> **Important:**\
> This project is **strictly for learning purposes**. It is **not intended for production use**. The code may contain bugs, security flaws, or features that require improvements or refactoring.

---

## Screenshots

![Home](https://github.com/user-attachments/assets/6355a8b8-5360-433f-b522-bfc4eb0c48f4)

![Contact List](https://github.com/user-attachments/assets/0b8bc7bf-551c-482c-893d-f85d3396011a)

![Single contact display](https://github.com/user-attachments/assets/1ed9ad36-9e6e-435c-9a04-bc6ecd2c02ba)

![Your Categories](https://github.com/user-attachments/assets/e34bb2f8-6ac3-4bce-bcfa-0edf9a6d4b84)

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

