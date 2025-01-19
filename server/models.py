from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin
metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    # Relationship to RestaurantPizza (with back_populates to establish the relationship)
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')

    def to_dict(self, exclude_pizzas=False):
        restaurant_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }

        if not exclude_pizzas:
            restaurant_dict['restaurant_pizzas'] = [pizza.to_dict() for pizza in self.pizzas]

        return restaurant_dict


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # Relationship to RestaurantPizza with explicit foreign key relationship
    restaurant_pizzas = db.relationship(
        'RestaurantPizza',
        back_populates='pizza',
        primaryjoin='Pizza.id == RestaurantPizza.pizza_id'  # Explicit primaryjoin
    )

    def to_dict(self, exclude_restaurant_pizzas=False):
        pizza_dict = {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
        }

        if not exclude_restaurant_pizzas and self.restaurant_pizzas:
            pizza_dict['restaurant_pizzas'] = [rp.to_dict() for rp in self.restaurant_pizzas]

        return pizza_dict

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    # Foreign key references the restaurant this pizza belongs to
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', back_populates='pizzas')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Validate price during initialization
        if self.price < 1 or self.price > 30:
            raise ValueError("Price must be between 1 and 30")

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id
        }
