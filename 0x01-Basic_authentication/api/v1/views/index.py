#!/usr/bin/env python3
"""Error handling and Requests"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Get the current status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Fetch statistics regarding the objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', strict_slashes=False)
def unauthorized() -> str:
    """
    GET /api/v1/unauthorized[/]
    Handle unauthorized access
    """
    abort(401)


@app_views.route('/forbidden', strict_slashes=False)
def forbidden() -> str:
    """
    GET /api/v1/forbidden[/]
    Handle forbidden access
    """
    abort(403)
