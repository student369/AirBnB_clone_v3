#!/usr/bin/python3
""" Modules """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
        Return JSON "status": "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """ count """
    k = ["Amenity", "City", "Place", "Review", "State", "User"]
    st = {"amenities": storage.count(k[0]),
          "cities": storage.count(k[1]),
          "places": storage.count(k[2]),
          "reviews": storage.count(k[3]),
          "states": storage.count(k[4]),
          "users": storage.count(k[5])}
    return jsonify(st)
