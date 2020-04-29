#!/usr/bin/python3
""""""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states_all():
    """Display all States"""
    states = []
    for v in storage.all(State).values():
        states.append(v.to_dict())
    return jsonify(states)


@app_views.route('/states/<id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_by_id(id):
    """States by id"""
    state = storage.get(State, id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        put = request.get_json()
        for k, v in put.items():
            if k == "name":
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict()), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_new():
    """New State"""
    if not request.json:
        abort(400, "Not a JSON")
    post = request.get_json()
    if "name" in post:
        n_state = State(**post)
        n_state.save()
        return jsonify(n_state.to_dict()), 201
    else:
        abort(400, "Missing name")
