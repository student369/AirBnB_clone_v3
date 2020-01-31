#!/usr/bin/python3
"""
Place endpoints
"""
from api.v1.views import app_views
from models import storage, Place
from flask import abort, request, jsonify


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['GET'])
def place_list(city_id):
    """
    Retrieves the list of all Place objects of a City
    ---
    parameters:
      - city_id:
        in: cities
        type: id
        required: true
        default: None
    definitions:
      Place:
        type: object
        properties:
      City:
        type: object
    responses:
      200:
        description: the list of all Place objects of a City
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def place_by_id(place_id):
    """
    Retrieves place by place id. If place_id not linked to place,
    raise 404.
    """
    places = storage.all("Place").values()
    place = next(filter(lambda x: x.id == place_id, places), None)
    return jsonify(place.to_dict()) if place else abort(404)


@app_views.route(
    '/places/<place_id>',
    strict_slashes=False,
    methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes place by id. If place_id not linked to place, raise 404
    Returns empty dict with status 200
    """
    places = storage.all("Place").values()
    place = next(filter(lambda x: x.id == place_id, places), None)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['POST'])
def create_place(city_id):
    """
    Creates new place. If request body not valid JSON, raises 400
    If dict does not contain 'name' key, raise 400
    Returns place object with status 201
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    kwargs = request.get_json()

    a = storage.get("City", city_id)
    if a is None:
        abort(404)

    if not kwargs.get('user_id'):
        abort(400, "Missing user_id")
    if not kwargs.get('name'):
        abort(400, 'Missing name')

    a = storage.get("User", kwargs['user_id'])
    if a is None:
        abort(404)

    my_place = Place(city_id=city_id, **kwargs)

    storage.new(my_place)
    storage.save()

    return jsonify(my_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """
    Updates place. If request not valid JSON, raises 400.
    If place_id not linked to place object, raise 404
    Returns place object with status code 200
    """
    places = storage.all("Place").values()
    place = next(filter(lambda x: x.id == place_id, places), None)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    args = request.get_json()

    for k, v in args.items():
        if k not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(place, k, v)
    storage.save()

    return jsonify(place.to_dict()), 200
    # might need to ignore keys explicityly


@app_views.route('/places/places_search',
                 strict_slashes=False, methods=['POST'])
def places_search():
    """ Searches for places."""
    if not request.get_json():
        abort(400, description="Not a JSON")
    args = request.get_json()

    states = args.get("states", None)
    cities = args.get("cities", None)
    amenities = args.get("amenities", None)

    if not states and not cities and not amenities:
        places = storage.all("Place").values()
        return jsonify(places), 200

    results = []

    if states:
        results.append({"states": "States"})
    if cities:
        results.append({"cities": "Cities"})
    if amenities:
        results.append({"amenities": "Amenity"})

    return jsonify(results), 200
