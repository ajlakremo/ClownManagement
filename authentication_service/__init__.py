from datetime import datetime, timezone, timedelta

from flask import Flask, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, create_access_token, set_access_cookies

from authentication_service.config import DevelopmentConfig
from authentication_service.models.models import db, User, Role, jwt, TokenBlocklist
from authentication_service.views.views import auth


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth, url_prefix='/')

    @app.errorhandler(404)
    def handle_bad_request(e):
        return jsonify({'error_code': 'Bad request.'}), 400

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({'error_code': 'Internal server error.'}), 500

    with app.app_context():
        db.create_all()

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        if isinstance(user, User):
            return user.id
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(id=identity).one_or_none()

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()['exp']
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            return response

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    return app
