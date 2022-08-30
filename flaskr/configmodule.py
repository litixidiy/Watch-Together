
ADDRESS = "0.0.0.0"
DB_SERVER  = "mongodb+srv://waterTest:sD5Vz6SU0A1bRE27@cluster0.afew3.mongodb.net/YouTubeWaterDB?retryWrites=true&w=majority"

class Config(object):
    """Base config, uses staging database server."""
    TESTING = False

class ProductionConfig(Config):
    """Uses production database server."""

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "dev"
    FLASK_ENV = 'development'

