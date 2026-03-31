# Mergington High School Activities API

A FastAPI application that allows students to view and sign up for extracurricular activities with persistent storage.

## Features

- View all available extracurricular activities
- Sign up for activities with persistent storage
- SQLite database with automatic initialization
- Capacity management for activities
- Student registration tracking

## Getting Started

1. Install the dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```
   The database will be automatically initialized on first run with seed data.

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc
   - Activities page: http://localhost:8000/static/index.html

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister from an activity                                     |

## Database

The application uses SQLite for persistent storage:

- **Database File**: `activities.db` (created in the working directory on first run)
- **Tables**:
  - `activities` - Activity records with name, description, schedule, and capacity
  - `participants` - Student emails
  - `activity_participants` - Many-to-many relationship between activities and students

Data is persisted and survives server restarts.

## Data Model

1. **Activities**:
   - `id` - Unique identifier
   - `name` - Activity name (unique)
   - `description` - Activity description
   - `schedule` - Schedule string
   - `max_participants` - Maximum capacity

2. **Participants**:
   - `email` - Student email (primary key)
   - Associated activities (many-to-many)
