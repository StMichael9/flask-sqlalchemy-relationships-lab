#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    event = Event.query.all()
    events_dict_list = []
    for e in event:
          events_dict_list.append({
        "id": e.id,
        "name": e.name,
        "location": e.location
    })
    return  make_response(jsonify(events_dict_list ),200)


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.filter_by(id=id).first()
    if not event:
        return make_response({"error": "Event not found"}, 404)
    sessions_list = []
    for s in event.sessions:
        sessions_list.append({
            "id": s.id,
            "title": s.title,
            "start_time": s.start_time.isoformat(),
    })
    return  make_response(jsonify(sessions_list ),200)

@app.route('/speakers')
def get_speakers():
    speaker = Speaker.query.all()
    speaker_dict_list = []
    for s in speaker:
        speaker_dict_list.append({
        "id": s.id,
        "name": s.name,
    })
    return make_response(jsonify(speaker_dict_list), 200)


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.filter_by(id=id).first()
    if not speaker:
        return make_response({"error": "Speaker not found"}, 404)
    speaker_data = {
    "id": speaker.id,
    "name": speaker.name,
    "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
    }
    return make_response(jsonify(speaker_data), 200)

        


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.filter_by(id=id).first()
    if not session:
         return make_response({"error": "Session not found"}, 404)
    session_list = []
    for s in session.speakers:
        session_list.append({
            "id": s.id,
            "name": s.name,
            "bio_text": s.bio.bio_text if s.bio else "No bio available"

    })
    return  make_response(jsonify(session_list ),200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)