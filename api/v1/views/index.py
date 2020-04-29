#!/usr/bin/python3
""""""
from flask import jsonify

from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """"""
    clss = {"Amenity": "amenities", "City": 'cities',
            "Place": "places", "Review": "reviews",
            "State": "states", "User": "users"}
    objs = {}
    for k, v in clss.items():
        objs[v] = storage.count(k)
    return jsonify(objs)
