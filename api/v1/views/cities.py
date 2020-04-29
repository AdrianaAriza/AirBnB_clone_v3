#!/usr/bin/python3
""""""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State

cities = storage.all('City')


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """"""
    objs = []
    try:
        for city in cities.values():
            if city.state_id == state_id:
                objs.append(city.to_dict())
        if len(objs):
            return jsonify(objs)
        else:
            abort(404)
    except:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_cities_id(city_id):
    """"""
    try:
        city = storage.get(City, city_id)
        if city.id == city_id:
            objs = []
            if request.method == 'GET':
                objs.append(city.to_dict())
                return jsonify(objs)
            if request.method == 'DELETE':
                city.delete()
                storage.save()
                return jsonify({}), 200
            if request.method == 'PUT':
                put = request.get_json()
                if not put:
                    abort(400, "Not a JSON")
                for k, v in put.items():
                    if k == "name":
                        setattr(city, k, v)
                storage.save()
                return jsonify(city.to_dict()), 200
        abort(404)
    except:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def new_city(state_id):
    """"""
    if not request.json:
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state and state.id == state_id:
        post = request.get_json()
        if "name" in post:
            post['state_id'] = state_id
            n_city = City(**post)
            n_city.save()
            return jsonify(n_city.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(404)
