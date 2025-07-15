# config.py

import os


# Get the absolute path of the directory where this file is located.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class. Contains default settings.
    Other configuration classes will inherit from this one.
    """
    # Set a default secret key. In production, this should be overridden
    # with a value from an environment variable for security.
    SECRET_KEY = os.environ.get('SECRET_KEY', '1qaz2wsx') # Default secret key for development.
    
    # Define the base data directory for the application.
    # This makes file paths more manageable and less prone to errors.
    DATA_DIR = os.path.join(basedir, 'gradebook_calc/data')
    
    # Define specific subdirectories within the data directory.
    CURRICULUM_DIR = os.path.join(DATA_DIR, 'curriculum')
    GRADES_DIR = os.path.join(DATA_DIR, 'grades')

    @staticmethod
    def init_app(app):
        """
        A hook for performing app-specific initializations.
        Can be used to set up logging, etc.
        """
        pass

class DevelopmentConfig(Config):
    """
    Development-specific configuration.
    Inherits from the base Config and overrides settings for development.
    """
    DEBUG = True
    # In development, you might use a simpler, predictable secret key.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

class ProductionConfig(Config):
    """
    Production-specific configuration.
    Inherits from the base Config and sets stricter settings for production.
    """
    # DEBUG must be False in production.
    DEBUG = False
    
    # In production, it's critical to use a strong, unique secret key
    # that is not stored in the code. It should be set as an environment variable.
    # The application will fail to start if SECRET_KEY is not set in the environment.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # For example, you could configure production logging here.
        # import logging
        # from logging.handlers import SysLogHandler
        # syslog_handler = SysLogHandler()
        # syslog_handler.setLevel(logging.WARNING)
        # app.logger.addHandler(syslog_handler)


# A dictionary to easily access the configuration classes by name.
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}