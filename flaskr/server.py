from datetime import timedelta

from flask import Flask, abort, jsonify, session ,request
from flask_socketio import SocketIO, join_room, leave_room, \
    close_room, disconnect
import flask_login

from pymongo.errors import DuplicateKeyError

import config
from db import get_user,save_user


'''
API 
Namespace:

time : recieves the time and make adjustment if needed
connect : is triggered when the client is successfully connected to the server
message : is triggered when the client sends data
join : is tiggered when the client 
disconnect : is triggered when the client loses the connection with the server, 
    -closing the browser, dropping the connection, etc.
'''

# Creating an instance of the Flask app
app = Flask(__name__)
app.secret_key = config.Config.SECRET_KEY

socketio = SocketIO(app, logger=True, engineio_logger=True,
                    cors_allowed_origins='*')

#allows flask_login to implemented into the Flask app
login_manager = flask_login.LoginManager()

#login_manager.login_view = "api/login"

#configure the flask app with the login manager
login_manager.init_app(app)

print("[Server Started] : " + config.Config.ADRESS)


@app.route('/')
def index():
    rooms = []

    
@app.route('/api/login', methods=['GET','POST'])
def login():

    if flask_login.current_user.is_authenticated:
        print('Logged in as: ' + flask_login.current_user.username)
        return {"msg":"isAuth"},200

    user = get_user(request.get_json().get('username'))

    password = request.get_json().get('password')
    print("[User Login] "+request.get_json().get('username') +" pw : "+request.get_json().get('password'))

    if user is None or password is None:
        return {"msg":"missing_field"},401
    
    if user and user.check_pw(password):
        print( "[User Msg] : {} Authenticated ".format(user.username))
        loggedIn =  flask_login.login_user(user,remember=True)
        
        if loggedIn:
            print("[User Msg] : "+flask_login.current_user.username +" Logged In")
        else:
            print("Login Failed")

        return {"msg":"auth"}, 200

    else:
        print( "[User Msg] : {} Not Authenticated ".format(user.username))
        return {"msg":"not_auth"}, 401

'''@app.route('/protected')
def protected():
    return 'Logged in as: ' + flask_login.current_user.id
'''
@app.route('/api/test', methods=['POST'])
def test():
    print(flask_login.current_user)
    return {"msg":"test"},200

#manage logout request
@app.route('/api/logout', methods=['POST'])
def logout():
    if flask_login.current_user.is_authenticated:
        print("[User Msg] : "+flask_login.current_user +" Logged Out")
        flask_login.logout_user()
        return {"msg":"logout"},200
    return {"msg":"not_auth&failed_to_logout"}

@app.route('/api/register', methods=['POST'])
def register():
    if flask_login.current_user.is_authenticated:
        return {"msg":"isAuth"},200

    username = request.get_json().get('username')
    password = request.get_json().get('password')

    try:
        save_user(username,password)
    except DuplicateKeyError:
        return {"msg":"username_duplicate"},401
    
    return {"msg":"register_success"},200


@login_manager.user_loader
def user_loader(username):
    print("[Server] : finding "+username)
    return get_user(username)


@login_manager.request_loader
def request_loader(request):
    if request.get_json() is None:
        return

    username = request.get_json().get('username')
    user = get_user(username)
    return user


if __name__ == '__main__':
    socketio.run(app, debug=config.Config.DEBUG)