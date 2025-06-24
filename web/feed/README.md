# Django Feed Simulator

This project was built as a learning exercise to practice fundamental Django concepts, focusing on database manipulation, templates, static files organization, and integration with external libraries like Faker.

---

## Purpose

- Practice the full Django workflow: URLs → Views → Models → Templates.
- Solidify understanding of Django's ORM for database operations.
- Organize static files and templates properly within the project structure.
- Automatically generate fake data using the Faker library (pt_BR locale).
- Implement a simple routine that deletes and recreates posts dynamically.

---

## Features

- A basic feed page that simulates simple posts.
- On every page load:
  - All existing posts are deleted.
  - New posts are automatically generated.
- Each post includes a fake author and content generated in Portuguese.
- A simple HTML and CSS interface to display the feed.

---

## Concepts Practiced

- Django project and app structure.
- Model definition with key fields (`author`, `content`, `created_at`).
- URL routing both at the project and app level.
- Function-based views with direct ORM interactions.
- Dynamic templates using inheritance, blocks, and for-loops.
- Static file management (CSS).
- Integration with the Faker library for generating realistic fake data.

---

## Technologies Used

- Python
- Django
- Faker (pt_BR locale)
- HTML & CSS

---
