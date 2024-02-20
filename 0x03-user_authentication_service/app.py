#!/usr/bin/env python3
"""User Auth Services"""
from flask import Flask, jsonify, request, make_response, redirect, abort
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handle unauthorized errors"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def unauthorized(error) -> str:
    """Handle forbidden errors"""
    return jsonify({"error": "Forbidden"}), 403


@app.route("/")
def home() -> str:
    """Home route"""
    return jsonify({"message": "Welcome"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """Register a new user"""
    email, password = request.form.get("email"), request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": "%s" % email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Login and set a session id"""
    email, password = request.form.get('email'), request.form.get('password')
    if AUTH.valid_login(email=email, password=password):
        res = make_response(
            jsonify({"email": "%s" % email, "message": "logged in"}))
        res.set_cookie("session_id", AUTH.create_session(email))
        return res
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logout a user"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    """Get and return user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Reset password"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": "%s" % email, "reset_token": "%s" % reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Update password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": "%s" % email, "message": "Password updated"})
    except Exception:
        pass
    abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
