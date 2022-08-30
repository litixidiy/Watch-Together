import os
from flask import Flask
from flask_socketio import SocketIO,disconnect
import flask_login
from flaskr.db import get_user, save_user
from flaskr.configmodule import DevelopmentConfig

socketio = SocketIO()

login_manager = flask_login.LoginManager()
@login_manager.user_loader
def user_loader(username):
    return get_user(username)

def create_app(test_config=None):
    """Create an application."""

    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # print("[Importing config]")
        app.config.from_object(DevelopmentConfig())
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import auth,vroom,events
    app.register_blueprint(auth.bp)
    app.register_blueprint(vroom.bp)
    app.register_blueprint(events.bp)
    
    app.add_url_rule('/', endpoint='index')

    print('[Server] Init APP')
    
    login_manager.init_app(app)
    socketio.init_app(app)

    return app
