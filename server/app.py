#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


# TODO: add functionality to all routes
@app.route("/events")
def get_events():
    """Return all events as a list of dicts."""
    events = Event.query.all()
    data = [
        {
            "id": event.id,
            "name": event.name,
            "location": event.location,
        }
        for event in events
    ]
    return jsonify(data), 200


@app.route("/events/<int:id>/sessions")
def get_event_sessions(id):
    """Return all sessions for a given event."""
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    sessions = [
        {
            "id": session.id,
            "title": session.title,
            "start_time": (
                session.start_time.isoformat()
                if session.start_time is not None
                else None
            ),
        }
        for session in event.sessions
    ]
    return jsonify(sessions), 200


@app.route("/speakers")
def get_speakers():
    """Return all speakers as a list of dicts."""
    speakers = Speaker.query.all()
    data = [
        {
            "id": speaker.id,
            "name": speaker.name,
        }
        for speaker in speakers
    ]
    return jsonify(data), 200


@app.route("/speakers/<int:id>")
def get_speaker(id):
    """Return a single speaker with their bio text."""
    speaker = Speaker.query.get(id)
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404

    bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"

    data = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text,
    }
    return jsonify(data), 200


@app.route("/sessions/<int:id>/speakers")
def get_session_speakers(id):
    """Return all speakers for a given session, including bio text."""
    session = Session.query.get(id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    speakers_data = []
    for speaker in session.speakers:
        bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
        speakers_data.append(
            {
                "id": speaker.id,
                "name": speaker.name,
                "bio_text": bio_text,
            }
        )

    return jsonify(speakers_data), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
