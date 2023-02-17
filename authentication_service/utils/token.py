from functools import wraps

import jwt
from flask import request, make_response, jsonify

from authentication_service import User, DevelopmentConfig


def decode_auth_token(token):
    try:
        payload = jwt.decode(token, DevelopmentConfig.SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired.'
    except jwt.InvalidTokenError:
        return 'Invalid token.'


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'A valid token is missing!'}), 401)
        try:
            data = decode_auth_token(token)
            current_user = User.query.get(int(data))
        except:
            return make_response(jsonify({'message': 'Invalid token!'}), 401)
        return f(current_user, *args, **kwargs)
    return decorator
