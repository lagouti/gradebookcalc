# gradebook_calc/__init__.py

from flask import Flask
import os
# import config object
from config import Config, config


def create_app(config_name='default'):
    """
    Application factory function.
    
    This function creates and configures the Flask application instance.
    Using a factory allows for creating different app instances for
    production, development, and testing, each with potentially
    different configurations.
    """
    
    # Create the Flask application object.
    # __name__ tells Flask where to look for resources like templates and static files.
    # 'templates' is the default folder, but it's good practice to be explicit.
    app = Flask(__name__, template_folder='templates')

    app.config.from_object(config[config_name])
    # This line allows the configuration to perform its own initializations if needed.
    config[config_name].init_app(app)

    # The application context is needed for certain Flask operations.
    # We push a context here to make the application instance available
    # for the blueprint registration.
    with app.app_context():
        # Import the blueprint from the routes module.
        # This is done inside the function to avoid circular imports.
        # If routes.py also needed to import 'app' from this module,
        # importing it at the top level would cause an error.
        from . import routes

        # Register the blueprint with the application.
        # A blueprint is a way to organize a group of related views and other code.
        # This keeps our application's routes modular.
        app.register_blueprint(routes.main_bp)

        # You could add more configurations here, such as:
        # - app.config.from_object('config.DevelopmentConfig')
        # - Initializing extensions like SQLAlchemy or LoginManager
        #   db.init_app(app)
        #   login_manager.init_app(app)

    return app


