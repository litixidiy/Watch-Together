
from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for)
import flask_login
from pymongo.errors import DuplicateKeyError

from flaskr.db import get_user, save_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

"""
    If the request method is POST, then get the username and password from the form, and if there are no
    errors, save the user to the database and redirect to the login page.
    If the request method is GET, then return the register html
    :return: a redirect to the login page.
"""


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        error = None
        if not email:
            error = 'Email is required'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                save_user(email, username, password)
            except DuplicateKeyError:
                error = f"User {username} is already registered."
            #redirect to login when no errors
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = get_user(username)

        if user is None:
            error = 'Incorrect username.'
        elif not user.check_pw(password):
            error = 'Incorrect password.'
        if error is None:
            loggedIn = flask_login.login_user(user, remember=True)
            if loggedIn:
                print("[User Msg] : " +
                      flask_login.current_user.username + " Logged In")
                return redirect(url_for('index'))
            else:
                print("[User Msg] : LogIn Failed")

        flash(error)
    return render_template('auth/login.html')


@bp.route('/logout')
@flask_login.login_required
def logout():
    if flask_login.current_user.is_authenticated:
        print("[User Msg] : "+flask_login.current_user.username + " Logged Out")
        flask_login.logout_user()
        return redirect(url_for('index'))
    return redirect(url_for('index'))
