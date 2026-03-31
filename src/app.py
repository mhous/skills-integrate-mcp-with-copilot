"""
High School Management System API

A FastAPI application that allows students to view and sign up for 
extracurricular activities at Mergington High School.

Features:
- Persistent storage using SQLite database
- RESTful API for activities and registrations
- Seed data initialization on first run
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from sqlalchemy.orm import Session
from database import init_db, get_db, Activity, Participant

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Initialize database on startup
init_db()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities with participant information"""
    activities = db.query(Activity).all()
    result = {}
    for activity in activities:
        result[activity.name] = {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": [p.email for p in activity.participants]
        }
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Validate activity exists
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    existing_participant = db.query(Participant).filter(
        Participant.email == email
    ).first()
    if existing_participant and existing_participant in activity.participants:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Validate activity is not at max capacity
    if len(activity.participants) >= activity.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Activity is at maximum capacity"
        )

    # Create or get participant
    participant = db.query(Participant).filter(
        Participant.email == email
    ).first()
    if not participant:
        participant = Participant(email=email)
        db.add(participant)
        db.flush()

    # Add student to activity
    activity.participants.append(participant)
    db.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    # Validate activity exists
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is signed up
    participant = db.query(Participant).filter(
        Participant.email == email
    ).first()
    if not participant or participant not in activity.participants:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student from activity
    activity.participants.remove(participant)
    db.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}
