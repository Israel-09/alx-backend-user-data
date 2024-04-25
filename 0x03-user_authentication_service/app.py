#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from flask import make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def home():
    """
    home path
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    create new user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return jsonify({"message": "Bad request"}), 400
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """implement login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged-in"})
        resp.set_cookie("session_id", session_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    implement logout
    """
    from sqlalchemy.orm.exc import NoResultFound

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'))
    abort(401)


@app.route('/profile', strict_slashes=False)
def profile():
    """returns user email"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_token():
    """get password reset token"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password():
    """reset password"""
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    email = request.form.get('email')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
