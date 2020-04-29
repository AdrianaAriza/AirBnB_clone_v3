#!/usr/bin/python3
""""""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenities_all():
    """Display all Amenities"""
    amenities = []
    for v in storage.all(Amenity).values():
        amenities.append(v.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenities_by_id(id):
    """Amenities by id"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        if request.method == 'GET':
            return jsonify(amenity.to_dict())
        if request.method == 'DELETE':
            amenity.delete()
            storage.save()
            return jsonify({}), 200
        if request.method == 'PUT':
            put = request.get_json()
            if not put:
                abort(400, "Not a JSON")
            for k, v in put.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(amenity, k, v)
            storage.save()
            return jsonify(amenity.to_dict()), 200
    except:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def amenity_new():
    """POST new Amenity"""
    if not request.json:
        abort(400, "Not a JSON")
    post = request.get_json()
    if "name" in post:
        n_amenity = Amenity(**post)
        n_amenity.save()
        return jsonify(n_amenity.to_dict()), 201
    else:
        abort(400, "Missing name")
