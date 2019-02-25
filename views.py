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
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        return getAllRestaurants()
    elif request.method == 'POST':
        mealType = request.args.get('mealType', '')
        location = request.args.get('location', '')
        return createNewRestaurant(mealType, location)

@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        return getRestaurant(id)
    elif request.method == 'PUT':
        name = request.args.get('name')
        address = request.args.get('address')
        image = request.args.get('image')
        return updateRestaurant(id, name, address, image)
    elif request.method == 'DELETE':
        return deleteRestaurant(id)


def getAllRestaurants():
    try:
        session = DBSession()
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[i.serialize for i in restaurants])
    except Exception as e:
        return jsonify({'error': 500, 'description': e})

def createNewRestaurant(mealType, location):
    try:
        restaurant = findARestaurant(mealType, location)
        session = DBSession()
        if restaurant != 'Unable to find a restaurant.':
            newRestaurant = Restaurant(
                    name = unicode(restaurant['name']),
                    address = unicode(restaurant['address']),
                    image = unicode(restaurant['image'])
                )
            session.add(newRestaurant)
            session.commit()
            return jsonify(newRestaurant.serialize)
        else:
            return jsonify({"error":"No Restaurants Found for %s in %s" % (mealType, location)})
    except Exception as e:
        return jsonify({'error': 500, 'description': e})

def getRestaurant(id):
    try:
        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(id = id).one()
        return jsonify(restaurant=restaurant.serialize)
    except Exception as e:
        return jsonify({
            'error': 404,
            'description': 'No restaurant found'
            })

def updateRestaurant(id, name, address, image):
    try:
        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(id=id).one()
        if name:
            restaurant.name = name
        if address:
            restaurant.address = address
        if image:
            restaurant.image = image
        session.add(restaurant)
        session.commit()
        return jsonify(restaurant.serialize)
    except Exception as e:
        return jsonify({'error': 500, 'description': e})

def deleteRestaurant(id):
    try:
        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(id=id).one()
        session.delete(restaurant)
        session.commit()
        return jsonify({
                'status': 200,
                'description': 'Restaurant {} deleted.'.format(id)
            })
    except Exception as e:
        return jsonify({'error': 500,
            'description': 'Unable to delete restaurant {}'.format(id),
            'message': str(e)
            })

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
