import json
import os

from flask import jsonify

from troupe_leader_service.services.AuthClient import BaseClient


class ClownClient(BaseClient):
    def __init__(self):
        self.base_url = os.getenv('CLOWN_SERVICE_URL')

    def create_appointment(self, endpoint='/api/clown/appointment', token='', data=None):
        headers = {
            'Authorization': 'Bearer ' + token,
        }

        res = self._make_request(method='POST', endpoint=endpoint, payload=data, additional_headers=headers)

        if res.status_code == 200:
            return json.loads(res.text)
        return jsonify({'message': 'Clown unavailable.'}), 400

