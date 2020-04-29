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
    try:
        state = storage.get(State, id)
        if request.method == 'GET':
            return jsonify(state.to_dict())
        if request.method == 'DELETE':
            state.delete()
            storage.save()
            return jsonify({}), 200
        if request.method == 'PUT':
            put = request.get_json()
            if not put:
                abort(400, "Not a JSON")
            for k, v in put.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(state, k, v)
            storage.save()
            return jsonify(state.to_dict()), 200
    except:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_new():
    """New State"""
    try:
        post = request.get_json()
        if "name" in post:
            new_state = State(**post)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        else:
            abort(400, "Missing name")
    except:
        abort(400, "Not a JSON")
