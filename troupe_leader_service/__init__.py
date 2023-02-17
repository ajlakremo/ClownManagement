from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from troupe_leader_service.config import DevelopmentConfig
from troupe_leader_service.views.views import troupe_leader_view

db = SQLAlchemy()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(troupe_leader_view, url_prefix='/')

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def handle_bad_request(e):
        return jsonify({'error_code': 'Bad request.'}), 400

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({'error_code': 'Internal server error.'}), 500

    return app

