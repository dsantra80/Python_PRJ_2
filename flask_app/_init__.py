from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Correct import path for config
    app.config.from_object('flask_app.config.Config')
    
    from .routes import routes
    app.register_blueprint(routes)

    return app
