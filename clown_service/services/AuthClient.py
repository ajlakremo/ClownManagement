import json
import os

import requests as requests
from flask import abort, jsonify

from clown_service.utils.constants import CLOWN_ROLE


class AuthClient:
    def __init__(self):
        self.base_url = os.getenv('AUTH_SERVICE_URL')

    def is_authorized(self, endpoint='/api/auth/verify', token=''):
        headers = {
            'Authorization': 'Bearer ' + token,
        }
        res = self._make_request(endpoint=endpoint, params={'role': CLOWN_ROLE}, additional_headers=headers)

        if res.status_code == 200:
            return True
        return False

    def get_user(self, endpoint='/api/user/{}', token='', user_id=''):
        headers = {
            'Authorization': 'Bearer ' + token,
        }

        endpoint = endpoint.format(user_id)

        res = self._make_request(endpoint=endpoint, additional_headers=headers)

        if res.status_code == 200:
            return json.loads(res.text)
        return jsonify({'message': 'User not found.'}), 400

    def _make_request(self, method='GET', endpoint=None, payload=None, additional_headers=None, params=None):
        headers = {
            'Content-Type': 'application/json',
        }

        if additional_headers:
            headers.update(additional_headers)

        if method == 'POST':
            return requests.post(self._get_url(endpoint),
                                 json=payload,
                                 headers=headers)
        elif method == 'GET':
            return requests.get(self._get_url(endpoint),
                                params=params,
                                headers=headers)
        elif method == 'PUT':
            return requests.put(self._get_url(endpoint),
                                json=payload,
                                headers=headers)
        elif method == 'DELETE':
            return requests.delete(self._get_url(endpoint),
                                   headers=headers)

    def _get_url(self, uri):
        return '%s%s' % (self.base_url, uri)
