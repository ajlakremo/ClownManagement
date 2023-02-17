from flask import Blueprint, request

from troupe_leader_service.services.ClownClient import ClownClient
from troupe_leader_service.utils.auth import extract_token, is_authorized

troupe_leader_view = Blueprint('troupe_leader_view', __name__)


@troupe_leader_view.route('api/appointment', methods=['POST'])
@is_authorized
def create_appointment():
    token = extract_token(request.headers)
    response = ClownClient().create_appointment(token=token, data=request.json)
    return response
