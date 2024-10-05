"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    results_1 = list(map(lambda user: user.serialize(), all_users))


    return jsonify(results_1), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id= user_id).first()


    return jsonify(user.serialize()), 200

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    results = list(map(lambda people: people.serialize(), all_people))

    return jsonify(results), 200


@app.route("/people/<int:people_id>", methods=['GET'])
def get_people_id(people_id):
    person = People.query.filter_by(id= people_id).first()

    return jsonify(person.serialize()), 200 
    
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    results_2 = list(map(lambda planet: planet.serialize(), all_planets))

    return jsonify(results_2), 200

@app.route("/planets/<int:planets_id>", methods=['GET'])
def get_planet_id(planets_id):
    planet = Planet.query.filter_by(id= planets_id).first()
    
    return jsonify(planet.serialize()), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    all_favorites = Favorite.query.filter_by(user_id=user_id).all()
    if len(all_favorites) <= 0:
        return jsonify({"error": "favorites not found"}), 404
    results = list(map(lambda favorite: favorite.serialize(), all_favorites))

    return jsonify(results), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def favorites_planets(user_id, planet_id):
    if user_id and planet_id:
        new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
    return jsonify(new_favorite.serialize())

@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def favorites_people(user_id, people_id):
    if user_id and people_id:
        new_favorite = Favorite(user_id=user_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()
    return jsonify(new_favorite.serialize())

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(user_id, planet_id):
    if user_id and planet_id:
        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if not favorite:
            return jsonify({"error": "favorite not found"}), 404
        db.session.delete(favorite)
        db.session.commit()
    return jsonify({"msg": "favorite removed successfully"}), 200

@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people(user_id, people_id):
    if user_id and people_id:
        favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if not favorite:
            return jsonify({"error": "favorite not found"}), 404
        db.session.delete(favorite)
        db.session.commit()
    return jsonify({"msg": "favorite removed successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
