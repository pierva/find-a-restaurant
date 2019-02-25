from findARestaurant import findARestaurant
from db_setup import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        return getAllRestaurants()
    elif request.method == 'POST':
        return createNewRestaurant(name, address, image)

@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        return getRestaurant(id)
    elif request.method == 'PUT':
        return
    elif request.method == 'DELETE':
        return


def getAllRestaurants():
    try:
        restaurants = session.query(Restaurant).all()
        return jsonify(Restaurants=[i.serialize for i in restaurants])
    except Exception as e:
        return jsonify(Error= {'code': 500})

def createNewRestaurant(name, address, image):
    try:
        restaurant = Restaurant(name = name, address = address, image = image)
        session.add(restaurant)
        session.commit()
        return jsonify(Restaurant=restaurant.serialize)
    except Exception as e:
        return jsonify(Error= {'code': 500})

def getRestaurant(id):
    try:
        restaurant = session.query(Restaurant).filter_by(id = id).one()
        return jsonify(restaurant=restaurant.serialize)
    except Exception as e:
        return jsonify(Error= {
            'code': 404,
            'description': 'No restaurant found'
            })


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
