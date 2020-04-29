#!/usr/bin/python3
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
        Return JSON "status": "OK"
    """
    return jsonify({"status": "OK"})
