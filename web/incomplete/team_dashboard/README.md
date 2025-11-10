# Team Dashboard

A full-stack web application for team collaboration and task management built with FastAPI and Jinja2 templating.

## PROJECT STATUS: INCOMPLETE LEARNING PROJECT

**Disclaimer**: This is an educational project created for learning purposes. It is not production-ready and lacks many features expected in a complete application. The code may contain bugs, security vulnerabilities, and incomplete functionality. This project was developed as a learning exercise in full-stack web development with FastAPI and may be abandoned or incomplete.

## Project Overview

Team Dashboard allows users to:
- Create and manage personal tasks
- Form teams and collaborate on team tasks
- Assign tasks to teams or keep them personal
- Manage team members with moderator privileges
- Track task status and deadlines

## Tech Stack

### Backend
- Framework: FastAPI (Python 3.8+)
- ORM: SQLAlchemy 2.0+
- Database: PostgreSQL (with SQLite support for development)
- Authentication: JWT (JSON Web Tokens)
- Password Hashing: Argon2
- Validation: Pydantic v2

### Frontend
- Templating: Jinja2
- Styling: Custom CSS with CSS variables for theming
- JavaScript: Vanilla JS for basic interactions

## Project Structure
```
team-dashboard/
├── app/
│ ├── core/
│ │ ├── auth.py
│ │ ├── config.py
│ │ ├── database.py
│ │ ├── dependencies.py
│ ├── models/
│ │ ├── user_model.py
│ │ ├── team_model.py
│ │ ├── team_member_model.py
│ │ ├── task_model.py
│ ├── routers/
│ │ ├── auth_routes.py
│ │ ├── user_routes.py
│ │ ├── team_routes.py
│ │ ├── task_routes.py
│ │ └── web/
│ ├── schemas/
│ │ ├── user_schema.py
│ │ ├── team_schema.py
│ │ ├── task_schema.py
│ ├── services/
│ │ ├── user_service.py
│ │ ├── team_service.py
│ │ ├── task_service.py
├── frontend/
│ ├── static/
│ │ └── css/
│ └── templates/
│ ├── auth/
│ ├── tasks/
│ ├── teams/
│ ├── user/
│ └── base.html
```


## Key Features Implemented

### Authentication & User Management
- User registration and login with JWT
- Password change functionality
- User profile management
- Secure password hashing with Argon2

### Task Management
- Create, read, update, and delete tasks
- Assign tasks to teams or keep as personal
- Task status tracking (pending, in progress, completed, cancelled)
- Due date management
- Task filtering and search

### Team Collaboration
- Team creation and management
- Team membership with moderator roles
- Team task assignment
- Member management (add/remove members)

### Frontend
- Responsive design with dark/light theme support
- Jinja2 templating for server-side rendering
- Custom CSS with consistent design system
- Form handling with validation

## Known Limitations & Incomplete Features

### Security
- Basic authentication implementation
- Limited input validation and sanitization
- No rate limiting or brute force protection
- Minimal error handling in some areas

### Functionality
- No real-time updates or WebSocket support
- Limited file upload capabilities
- No advanced search or filtering
- Missing email verification
- No password reset functionality
- Limited error handling and user feedback

### UI/UX
- Basic responsive design
- Limited accessibility features
- No progressive enhancement
- Basic form validation only

### Database
- Simple relationships without advanced query optimization
- Limited indexing and performance considerations
- Basic migration system

## Installation & Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (database URL, secret keys)
```.env
# Database Configuration
DATABASE_URL=postgresql://postgres:@localhost:5432/team_dashboard

# Application Settings
DEBUG=True

# JWT Security Configuration
JWT_SECRET_KEY=123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
4. Run database migrations
5. Start the server: `uvicorn app.main:app --reload`

## Development Notes

This project was developed as a learning exercise to understand:
- FastAPI framework and modern Python web development
- SQLAlchemy ORM and database modeling
- JWT authentication implementation
- Server-side rendering with Jinja2
- Full-stack application architecture
- CSS theming and responsive design

## Contributing

As this is a learning project, contributions are not actively sought. 

## License

This project is provided as-is for educational purposes. No specific license is applied.

## Warning

This application is not suitable for production use. It lacks essential security features, proper error handling, and comprehensive testing.
