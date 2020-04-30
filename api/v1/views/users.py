#!/usr/bin/python3
""""""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def users_all():
    """"""
    users = []
    for v in storage.all(User).values():
        users.append(v.to_dict())
    return jsonify(users)


@app_views.route('/users/<id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_by_id(id):
    """"""
    user = storage.get(User, id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        put = request.get_json()
        for k, v in put.items():
            if k not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def user_new():
    """"""
    if not request.json:
        abort(400, "Not a JSON")
    post = request.get_json()
    if "email" in post:
        if "password" in post:
            n_user = User(**post)
            n_user.save()
        else:
            abort(400, "Missing password")
        return jsonify(n_user.to_dict()), 201
    abort(400, "Missing email")
