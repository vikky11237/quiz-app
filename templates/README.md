# Quiz App Documentation

## Overview
A Flask-based quiz application that allows users to take quizzes, track scores, and manage questions through an admin interface.

## Project Structure
quiz_app/
├── app.py # Main application file
├── models.py # Database models
├── init_db.py # Database initialization
├── quiz.db # SQLite database
├── README.md # Documentation
└── templates/ # HTML templates
├── admin/
│ └── manage_questions.html
├── base.html
├── index.html
└── quiz.html

## Features
- User Authentication
- Random Quiz Generation (5 questions per quiz)
- Score Tracking and History
- Admin Question Management
- Category-based Questions
- Progress Tracking
- Responsive Design

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup Steps
1. Clone the repository
2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install flask flask-sqlalchemy flask-login werkzeug
```

4. Initialize database:
```bash
python init_db.py
```

5. Run application:
```bash
flask run
```

## Database Models

### User Model
```python:quiz_app/models.py
startLine: 8
endLine: 21
```

### Category Model
```python:quiz_app/models.py
startLine: 23
endLine: 26
```

### Question Model
```python:quiz_app/models.py
startLine: 28
endLine: 37
```

## Routes

### Public Routes
- `/login` - User login
- `/register` - New user registration
- `/logout` - User logout

### Protected Routes
- `/` - Homepage with recent scores
- `/quiz` - Take a quiz (5 random questions)
- `/profile` - User profile and statistics

### Admin Routes
- `/admin/questions` - Manage questions
- `/admin/question/add` - Add new questions

## Admin Access
Default admin credentials:
- Username: admin
- Password: admin123

## Quiz Flow
1. User clicks "Start Quiz"
2. System selects 5 random questions from all categories
3. User answers questions one at a time
4. Progress bar shows completion status
5. Final score displayed with pass/fail status (70% passing threshold)
6. Score saved to database

## Database Management

### Using DB Browser for SQLite
1. Download from: https://sqlitebrowser.org/
2. Open quiz.db file
3. Browse/edit data directly

### Using Python Shell
```python
from app import app, db
from models import User, Question, Category, QuizScore

with app.app_context():
    # Query examples
    users = User.query.all()
    questions = Question.query.all()
    categories = Category.query.all()
```

## Security Features
1. Password Hashing (Werkzeug)
2. Login Required Protection
3. Admin Required Protection
4. Session Management
5. CSRF Protection

## Template Structure
- base.html: Main layout template
- index.html: Homepage with quiz history
- quiz.html: Quiz interface
- admin/manage_questions.html: Question management

## Error Handling
- Database connection errors
- Authentication errors
- Quiz validation
- Admin access control

## Contributing
1. Fork the repository
2. Create feature branch
3. Submit pull request

## License
MIT License

Would you like me to expand on any particular section or add additional documentation?
