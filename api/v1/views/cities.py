#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET', "POST"])
def get_cities(state_id):
    """"""
    objs = []
    try:
        cities = storage.all('City')
        for city in cities.values():
            if city.state_id == state_id:
                objs.append(city.to_dict())
            if len(objs):
                return jsonify(objs)
            else:
                abort(404)
    except:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def get_cities_id(city_id):
    """"""
    objs = []
    try:
        cities = storage.all('City')
        for city in cities.values():
            if city.id == city_id:
                if request.method == 'GET':
                    objs.append(city.to_dict())
                elif request.method == 'DELETE':
                    city.delete()
                    storage.save()
                    return jsonify({}), 200
                elif request.method == 'PUT':
                    put = request.get_json()
                    if not put:
                        abort(400, "Not a JSON")
                    for k, v in put.items():
                        if k == "name":
                            setattr(city, k, v)
                    storage.save()
                    return jsonify(city.to_dict()), 200
        if len(objs):
            return jsonify(objs)
        else:
            abort(404)
    except:
        abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def new_city(state_id):
    """"""
    try:
        cities = storage.all('City')
        for city in cities.values():
            if city.state_id == state_id:
                post = request.get_json()
                post['state_id'] = state_id
                if "name" in post:
                    n_city = City(**post)
                    n_city.save()
                    return jsonify(n_city.to_dict()), 201
                else:
                    abort(400, "Missing name")
    except:
        abort(400, "Not a JSON")