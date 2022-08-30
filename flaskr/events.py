import functools
from flask import session,Blueprint
import flask_login
from flask_socketio import emit, join_room, leave_room,disconnect
from flaskr.db import get_most_recent_state, save_state
from . import socketio

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not flask_login.current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped
    
bp = Blueprint('events',__name__)


@socketio.on('test',namespace='/vroom')
def handle_test(msg):
    room_id = msg['room_id']
    emit('set_time',{'time':10})

@socketio.on('state',namespace = '/vroom')
def handle_state(msg):
    room_id = msg['room_id']
    save_state(room_id,msg)
    emit('state',msg, to=room_id)


@socketio.on('get_most_recent_state',namespace='/vroom')
def handle_get_most_recent_state(msg):
    return get_most_recent_state(msg['room_id']);



@socketio.on('join', namespace='/vroom')
def handle_join(msg):
    """
    When a user joins a room, emit a message to the room that the user has joined.
    
    :param msg: The message sent from the client
    """
    room_id = msg['room_id']
    user = flask_login.current_user.username

    join_room(room_id)

    emit('status', {'msg':user+' has entered the room.'},to=room_id )

@socketio.on('left', namespace='/vroom')
def left(msg):
    """
    It takes the room_id from the message, leaves the room, and then emits a status message to the room
    :param msg: The message sent by the client
    """
    
    user = flask_login.current_user.username
    room_id = msg['room_id']

    emit('status', {'msg': user+ ' has left the room.'},to=room_id)
    leave_room(room_id)