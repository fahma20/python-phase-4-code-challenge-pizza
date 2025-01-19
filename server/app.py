#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False  # Ensures the JSON response is not compacted

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return make_response(jsonify([restaurant.to_dict(exclude_pizzas=True) for restaurant in restaurants]), 200)


@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)
    return make_response(jsonify(restaurant.to_dict()), 200)


@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)

    # Cascade delete via relationships (RestaurantPizza entries will be deleted automatically)
    db.session.delete(restaurant)
    db.session.commit()
    return make_response("", 204)  # No content


@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return make_response(jsonify([pizza.to_dict(exclude_restaurant_pizzas=True) for pizza in pizzas]), 200)


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    pizza_id = data['pizza_id']
    restaurant_id = data['restaurant_id']
    price = data['price']

    # Validation for price range
    if price < 1 or price > 30:
        return make_response(jsonify({'errors': ['validation errors']}), 400)

    # Fetch the pizza and restaurant objects
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({'errors': ['Pizza or Restaurant not found']}), 404

    # Create a new RestaurantPizza object
    restaurant_pizza = RestaurantPizza(
        price=price,
        pizza_id=pizza_id,
        restaurant_id=restaurant_id
    )

    db.session.add(restaurant_pizza)
    db.session.commit()

    # Return the response including pizza and restaurant information
    return jsonify({
        'id': restaurant_pizza.id,
        'price': restaurant_pizza.price,
        'pizza_id': restaurant_pizza.pizza_id,
        'restaurant_id': restaurant_pizza.restaurant_id,
        'pizza': pizza.to_dict(exclude_restaurant_pizzas=True),  # Ensure pizza details are returned
        'restaurant': {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }
    }), 201
