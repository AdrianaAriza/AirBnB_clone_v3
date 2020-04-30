#!/usr/bin/python3
""""""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    objs = []
    for place in places.values():
        if place.city_id == city_id:
            objs.append(place.to_dict())
    return jsonify(objs)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_places_id(place_id):
    """"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        put = request.get_json()
        for k, v in put.items():
            if k not in ["id", "user_id", "city_id",
                         "created_at", "updated_at"]:
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def new_place(city_id):
    """"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    post = request.get_json()
    if "name" in post:
        post['city_id'] = city_id
        if "user_id" in post:
            user = storage.get(User, post['user_id'])
            if user is None:
                abort(404)
            if "name" in post:
                n_place = Place(**post)
                n_place.save()
                return jsonify(n_place.to_dict()), 201
            else:
                abort(400, "Missing name")
        else:
            abort(400, "Missing user_id")
    else:
        abort(400, "Missing name")
