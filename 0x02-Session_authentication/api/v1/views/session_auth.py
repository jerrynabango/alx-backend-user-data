#!/usr/bin/env python3
"""User Authentication Views"""

import os
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.user import User

@app_views.route('/session/login', methods=['POST'], strict_slashes=False)
def login_session() -> str:
    """Log in user with session authentication"""
    email, password = request.form.get('email'), request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_cookie_name = os.getenv('SESSION_NAME')
    session_id = auth.create_session(user[0].id)
    response = make_response(jsonify(user[0].to_json()))
    if session_cookie_name and session_id:
        response.set_cookie(session_cookie_name, session_id)
    return response

@app_views.route('/session/logout', methods=['DELETE'], strict_slashes=False)
def logout_session(user_id: str = None) -> str:
    """Log out user by destroying session"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
