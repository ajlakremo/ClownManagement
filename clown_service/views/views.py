from datetime import datetime

from flask import jsonify, Blueprint, request, make_response

from clown_service.models.models import Appointment, db, AppointmentSchema, AppointmentIssue, AppointmentIssueSchema
from clown_service.services.AuthClient import AuthClient
from clown_service.utils.auth import extract_token, is_authorized

clown = Blueprint('clown', __name__)
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
appointment_issue_schema = AppointmentIssueSchema()


@clown.route('api/clown/appointments', methods=['GET'])
@is_authorized
def get_appointments():
    token = extract_token(request.headers)
    user = AuthClient().get_user(token=token)

    appointments = Appointment.query.filter_by(clown_id=user['id']).all()
    result = appointments_schema.dump(appointments)
    return jsonify(result), 200


@clown.route('api/clown/raise-issue/<appointment_id>', methods=['PUT'])
@is_authorized
def raise_issue(appointment_id):
    if not Appointment.query.filter_by(id=appointment_id).first():
        return jsonify({'message': 'Appointment does not exist.'}), 400
    
    appointment_issue = AppointmentIssue(appointment_id=appointment_id, **request.json)
    db.session.add(appointment_issue)
    db.session.commit()

    result = appointment_issue_schema.jsonify(appointment_issue)
    return result, 200


@clown.route('api/clown/appointment', methods=['POST'])
def create_appointment():
    if Appointment.query.filter(Appointment.clown_id == request.json.get('clown_id'),
                                Appointment.start >= request.json.get('start'),
                                Appointment.end <= request.json.get('end')).first():
        return make_response(jsonify({'message': 'Clown unavailable.'}), 400)

    appointment = Appointment(**request.json)

    db.session.add(appointment)
    db.session.commit()
    return appointment_schema.jsonify(appointment), 200


@clown.route('api/client/contact-details/<client_id>', methods=['GET'])
@is_authorized
def get_client_contact_details(client_id):
    token = extract_token(request.headers)
    user = AuthClient().get_user(token=token, user_id=client_id)
    return user


@clown.route('api/clown/appointments/<client_id>', methods=['GET'])
def get_client_appointments(client_id):
    completed = request.args.get('completed', type=lambda v: v.lower() == 'true')
    appointments = Appointment.query.filter(Appointment.client_id == client_id)

    if completed:
        appointments = appointments.filter(Appointment.end <= datetime.utcnow())
    elif completed is not None and not completed:
        appointments = appointments.filter(Appointment.end >= datetime.utcnow())

    return jsonify(appointments_schema.dump(appointments.all())), 200


@clown.route('api/clown/appointment/<appointment_id>', methods=['PUT'])
def rate_appointment(appointment_id):
    score = request.json.get('score')

    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    appointment.score = score

    db.session.commit()
    return appointment_schema.jsonify(appointment), 200
