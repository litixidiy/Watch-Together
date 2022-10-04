from flask import Flask
from flask_socketio import SocketIO
import flask_login
from flaskr.db import get_user

socketio = SocketIO()

def create_app(test_config=None):
    """Create an application."""
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    
    from . import auth,vroom,events
    app.register_blueprint(auth.bp)
    app.register_blueprint(vroom.bp)
    app.register_blueprint(events.bp)
    
    app.add_url_rule('/', endpoint='index')

    print('[Server] Init APP')
    
    login_manager = flask_login.LoginManager()
    @login_manager.user_loader
    def user_loader(username):
        return get_user(username)

    login_manager.init_app(app)
    socketio.init_app(app)

    return app