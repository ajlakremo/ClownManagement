from datetime import datetime

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clown_id = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer)


class AppointmentIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    appointment = db.relationship('Appointment', lazy=True)
    issue = db.Column(db.Text, nullable=False)
    resolved = db.Column(db.Boolean, default=False)


class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment


class AppointmentIssueSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AppointmentIssue
        fields = ['id', 'issue', 'resolved', 'appointment_id']


