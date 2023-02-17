import json
import os

from flask import abort

from troupe_leader_service.services.AuthClient import BaseClient


class ClownClient(BaseClient):
    def __init__(self):
        self.base_url = os.getenv('CLOWN_SERVICE_URL')

    def get_appointments(self, endpoint='/api/clown/appointments/{}', client_id='', params=None):
        endpoint = endpoint.format(client_id)

        res = self._make_request(endpoint=endpoint, params=params)

        if res.status_code == 200:
            return json.loads(res.text)
        return abort(400)

    def rate_appointment(self, endpoint='/api/clown/appointment/{}', appointment_id='', data=None):
        endpoint = endpoint.format(appointment_id)

        res = self._make_request(method='PUT', endpoint=endpoint, payload=data)

        if res.status_code == 200:
            return json.loads(res.text)
        return abort(400, {'message': 'Appointment does not exist'})

