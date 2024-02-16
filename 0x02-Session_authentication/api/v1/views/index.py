#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/system-status', methods=['GET'], strict_slashes=False)
def system_status() -> str:
    """Returns the status of the API system"""
    return jsonify({"system_status": "Operational"})


@app_views.route('/system-stats/', strict_slashes=False)
def system_stats() -> str:
    """Returns statistics about the objects in the system"""
    from models.user import User
    stats_data = {}
    stats_data['user_count'] = User.count()
    return jsonify(stats_data)


@app_views.route('/authentication-error', strict_slashes=False)
def authentication_error() -> str:
    """Returns an error message indicating authentication failure"""
    abort(401)


@app_views.route('/authorization-error', strict_slashes=False)
def authorization_error() -> str:
    """Returns an error message indicating authorization failure"""
    abort(403)
