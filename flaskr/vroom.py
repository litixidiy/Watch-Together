from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
import flask_login
import re

from flaskr.db import add_room_member, get_room, get_room_members, get_room_of_user, get_user, is_room_admin, is_room_member,save_room

bp = Blueprint('vroom',__name__)

def youtube_url_parser(url):
    """
    It takes a youtube url and returns the video id
    
    :param url: The URL of the video you want to embed
    :return: A match object
    """
    regExp = '^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*'
    match = re.match(regExp, url)
    return match



@bp.route('/')
def index():
    """
    It renders the index.html template, passing in the rooms variable, which is a list of rooms that the
    current user is a member of
    :return: The index.html template is being returned.
    """

    rooms =[]
    if flask_login.current_user.is_authenticated:
        rooms = get_room_of_user(flask_login.current_user.username)
    
    return render_template('vroom/index.html',rooms = rooms)


@bp.route('/create', methods=('GET', 'POST'))
@flask_login.login_required
def create():
    """
    If the request method is POST, then get the roomname from the form, and if the roomname is not
    empty, then save the roomname and the current user's username to the database, and then redirect to
    the index page.
    
    If the request method is not POST, then render the create.html template.
    :return: the rendered template for the create.html page.
    """

    if request.method == 'POST':
        vid_id = youtube_url_parser(request.form['vid_id'])[7]
        
        error = None
        if not vid_id:
            error = 'Unvalid Video Name'
        if error is not None:
            flash(error)
        else:
            room_id = save_room(vid_id,flask_login.current_user.username)
            return redirect(url_for("vroom.view_vroom",room_id=room_id))
    return render_template('vroom/create.html')


@bp.route('/vroom/<room_id>/', methods=('GET', 'POST'))
@flask_login.login_required
def view_vroom(room_id):
    """
        If the user is logged in, and the room exists, and the user is a member of the room, then render the
        vroom.html template.
        
        :param room_id: The unique identifier for the room
        :return: a tuple of two values. The first value is a string, and the second value is an integer.
    """

    room_obj = get_room(room_id)
    is_admin = is_room_admin(room_id,flask_login.current_user.username )
    
    if request.method == 'POST':
        username = request.form['username']
        add_room_member(room_id,room_obj["vid_id"],username,False)
        return ('', 204)

    else:
        if room_obj and is_room_member(room_id=room_id,username = flask_login.current_user.username):
            return render_template('vroom/vroom.html',username = flask_login.current_user.username,room_obj= room_obj,is_admin = is_admin )
        return "Room not found",404


@bp.route('/vroom/<room_id>/edit')
@flask_login.login_required
def edit_vroom(room_id):
    """
    If the request method is POST, then check if the room exists, if the user is a member of the room,
    and if the user is an admin of the room. If all of those conditions are met, then render the vroom
    template. Otherwise, return a 404 error
    
    :param room_id: The id of the room to be edited
    :return: a string.
    """

    if request.method == 'POST':
        room_obj = get_room(room_id)
        if room_obj and is_room_member(room_id=room_id,username = flask_login.current_user.username) and is_room_admin(room_id,flask_login.current_user.username ):
            return render_template('vroom/vroom.html',username = flask_login.current_user.username,room_obj= room_obj)
        return "Room not found",404
    return render_template('vroom/edit_vroom.html')


