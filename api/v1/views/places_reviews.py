#!/usr/bin/python3
""""""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review)
    objs = []
    for review in reviews.values():
        if review.place_id == place_id:
            objs.append(review.to_dict())
    return jsonify(objs)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_reviews_id(review_id):
    """"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        put = request.get_json()
        for k, v in put.items():
            if k not in ["id", "user_id", "place_id",
                         "created_at", "updated_at"]:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def new_review(place_id):
    """"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    post = request.get_json()
    if "name" in post:
        post['place_id'] = place_id
        if "user_id" in post:
            user = storage.get(User, post['user_id'])
            if user is None:
                abort(404)
            if "text" in post:
                n_review = Review(**post)
                n_review.save()
                return jsonify(n_review.to_dict()), 201
            else:
                abort(400, "Missing text")
        else:
            abort(400, "Missing user_id")
    else:
        abort(400, "Missing name")
