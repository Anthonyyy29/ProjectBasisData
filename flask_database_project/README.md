# Flask Database Project

A Flask web application with database integration using SQLAlchemy.

## Project Structure

```
flask_database_project/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── models/              # Database models
│   │   └── __init__.py
│   ├── routes/              # Application routes/endpoints
│   │   ├── __init__.py
│   │   └── main.py
│   ├── templates/           # HTML templates
│   │   └── index.html
│   └── static/              # Static files (CSS, JS, images)
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       └── images/
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── .gitignore              # Git ignore rules
```

## Setup Instructions

1. **Create a virtual environment:**
   ```bash
   cd flask_database_project
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## Features

- Flask application with modular structure
- SQLAlchemy database integration
- RESTful API endpoints
- HTML templates with Jinja2
- Static file serving (CSS, JavaScript)
- Configuration management for different environments
- User model example

## Database Models

The project includes a basic `User` model as an example. You can add more models in the `app/models/` directory.

## API Endpoints

- `GET /` - Main page
- `GET /api/users` - Get all users

## Configuration

Configuration settings are managed in `config.py` with support for:
- Development
- Production
- Testing

## Development

To add new features:
1. Create models in `app/models/`
2. Create routes in `app/routes/`
3. Create templates in `app/templates/`
4. Add static files in `app/static/`
