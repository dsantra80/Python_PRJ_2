from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Register blueprints
    from .routes import routes
    app.register_blueprint(routes)

    return app
