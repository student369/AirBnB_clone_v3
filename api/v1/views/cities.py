#!/usr/bin/python3
"""
City endpoints
"""
from api.v1.views import app_views
from models import storage, City
from flask import abort, request, jsonify


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False,
    methods=['GET'])
def city_by_state_id(state_id):
    """
    Retrieves list of all City objects of a State
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_by_id(city_id):
    """
    Retrieves city by city id. If city_id not linked to City,
    raise 404.
    """
    cities = storage.all("City").values()
    city = next(filter(lambda x: x.id == city_id, cities), None)
    return jsonify(city.to_dict()) if city else abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes city by id. If city_id not linked to City, raise 404
    Returns empty dict with status 200
    """
    cities = storage.all("City").values()
    city = next(filter(lambda x: x.id == city_id, cities), None)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False,
    methods=['POST'])
def create_city(state_id):
    """
    Creates new city. If request body not valid JSON, raises 400
    If state_id not linked to State, raise 404
    If dict does not contain 'name' key, raise 400
    Returns city object with status 201
    """

    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")

    a = storage.get("State", state_id)
    if a is None:
        abort(404)

    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    my_city = City(**kwargs)

    storage.new(my_city)
    storage.save()

    return jsonify(my_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """
    Updates city. If request not valid JSON, raises 400.
    If city_id not linked to City object, raise 404
    Returns city object with status code 200
    """
    cities = storage.all("City").values()
    city = next(filter(lambda x: x.id == city_id, cities), None)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    args = request.get_json()

    for k, v in args.items():
        if k not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, k, v)
    storage.save()

    return jsonify(city.to_dict()), 200
