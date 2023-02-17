from datetime import datetime, timezone

from flask import request, Blueprint, jsonify, make_response, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, current_user
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from authentication_service import User, db, TokenBlocklist, Role
from authentication_service.models.models import UserSchema, RoleSchema
from authentication_service.utils.validate import validate_registration

auth = Blueprint('auth', __name__)
user_schema = UserSchema()
role_schema = RoleSchema(many=True)


@auth.route('api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            token = create_access_token(identity=user)
            user_json = user_schema.dump(user)
            user_json["token"] = token
            return user_json, 200

        return make_response(jsonify({'message': 'User does not exists.'}), 401)
    return make_response({'message': 'Login.'}, 200)


@auth.route('api/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('api/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.pop('confirm_password')
    role = request.json.pop('role')

    try:
        validate_registration(email, password, confirm_password)
        new_user = User(**request.json)
        new_user.roles.append(Role.query.filter_by(name=role).first())
        db.session.add(new_user)
        try:
            db.session.commit()
        except SQLAlchemyError as exc:
            return {'error': str(exc)}, 400

        return user_schema.jsonify(new_user)

    except ValidationError as e:
        return jsonify({'message': e.messages}), 400


@auth.route('api/user/<user_id>', methods=['GET'])
@auth.route('api/user/', defaults={'user_id': None})
@jwt_required()
def get_user(user_id=None):
    if user_id:
        user = User.query.get(int(user_id))
        return user_schema.jsonify(user), 200

    return user_schema.jsonify(current_user), 200


@auth.route('api/auth/verify', methods=['GET'])
@jwt_required()
def auth_verify_user():
    role = request.args.get('role', default='', type=str)
    role = Role.query.filter_by(name=role).first()

    if role not in current_user.roles:
        return jsonify({'message': 'Access denied.'}), 401
    return jsonify({'message': 'Successful'}), 200


@auth.route('api/roles', methods=['GET'])
def roles():
    role = Role.query.all()
    result = role_schema.dump(role)
    return jsonify(result), 200
