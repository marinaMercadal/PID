from flask import Flask
from app.extensions import db
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app.agenda.routes import agenda_bp
    app.register_blueprint(agenda_bp)

    with app.app_context():
        db.create_all()

    return app