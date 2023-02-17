from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from client_service.config import DevelopmentConfig
from client_service.views.views import client_view

db = SQLAlchemy()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(client_view, url_prefix='/')
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({'error_code': e.description.get('message', '')}), 400

    @app.errorhandler(404)
    def handle_bad_request(e):
        return jsonify({'error_code': 'Bad request.'}), 400

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({'error_code': 'Internal server error.'}), 500

    with app.app_context():
        db.create_all()

    return app

