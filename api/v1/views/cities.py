#!/usr/bin/python3
""""""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City)
    objs = []
    for city in cities.values():
        if city.state_id == state_id:
            objs.append(city.to_dict())
    return jsonify(objs)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_cities_id(city_id):
    """"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        put = request.get_json()
        for k, v in put.items():
            if k == "name":
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def new_city(state_id):
    """"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    post = request.get_json()
    if "name" in post:
        post['state_id'] = state_id
        n_city = City(**post)
        n_city.save()
        return jsonify(n_city.to_dict()), 201
    else:
        abort(400, "Missing name")
