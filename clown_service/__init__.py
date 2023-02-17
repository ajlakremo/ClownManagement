from flask import Flask, jsonify

from clown_service.config import DevelopmentConfig
from clown_service.models.models import db, ma
from clown_service.views.views import clown


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(clown, url_prefix='/')

    @app.errorhandler(404)
    def handle_bad_request(e):
        return jsonify({'error_code': 'Bad request.'}), 400

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({'error_code': 'Internal server error.'}), 500

    with app.app_context():
        db.create_all()

    return app

