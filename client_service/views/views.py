from flask import jsonify, Blueprint, request
from flask_jwt_extended import current_user, jwt_required

from client_service.services.AuthClient import AuthClient
from client_service.services.ClownClient import ClownClient
from client_service.utils.auth import is_authorized, extract_token

client_view = Blueprint('client_view', __name__)


@client_view.route('api/client/appointments', methods=['GET'])
@is_authorized
def get_appointments():
    token = extract_token(request.headers)
    user = AuthClient().get_user(token=token)

    params = request.args.to_dict()
    appointments = ClownClient().get_appointments(client_id=user["id"], params=params)
    return jsonify(appointments), 200


@client_view.route('api/client/rate-appointment/<appointment_id>', methods=['PUT'])
@is_authorized
def rate_appointment(appointment_id):
    appointment = ClownClient().rate_appointment(appointment_id=appointment_id, data=request.json)
    return jsonify(appointment), 200