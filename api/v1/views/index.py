#!/usr/bin/python3
""" index """

from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage


@app_views.route('/status')
def status():
    """status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def count():
    """ count """
    keys = ["Amenity", "BaseModel", "City", "Place", "Review", "State", "User"]
    st = {"amenities": None,
          "cities": None,
          "places": None,
          "reviews": None,
          "states": None,
          "users": None}
    for k, y in zip(st.keys(), keys):
        st[k] = storage.count(y)
    return jsonify(st)
