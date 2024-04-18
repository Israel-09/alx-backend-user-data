#!/usr/bin/env python3
"""
views for session authentication
"""
from api.v1.views import app_views
from flask import request, jsonify, make_response, abort
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def retieve_user():
    """
    retrieves user instance from credentials
    """
    from api.v1.app import auth

    u_mail = request.form.get('email')
    if not u_mail:
        return jsonify({"error": "email missing"}), 400
    u_pass = request.form.get('password')
    if not u_pass:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": u_mail})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if user.is_valid_password(u_pass) is False:
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    session_name = getenv('SESSION_NAME')
    resp = make_response(jsonify(user.to_json()))
    resp.set_cookie(session_name, session_id)
    return resp


@app_views.route("/auth_session/logout",
                 methods=['DELETE'], strict_slashes=False)
def logout_session():
    """
    delete a session instance
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
