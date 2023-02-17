from functools import wraps

from flask import request, jsonify

from troupe_leader_service.services.AuthClient import AuthClient


def is_authorized(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return jsonify({'message': 'Access denied.'}), 401

        token = extract_token(request.headers)

        if AuthClient().is_authorized(token=token):
            return function(*args, **kwargs)
        return jsonify({'message': 'Access denied.'}), 401

    return decorator


def extract_token(headers):
    bearer = headers.get('Authorization')
    token = bearer.split()[1]

    return token
