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
from models import db, User, Planets, Species, People

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


################   ENDPOINTS PARA USUARIOS ##################

@app.route('/users', methods=['GET'])
def get_all_user():
    users = User.query.all()
    status_code = 400 if users is None else 200
    return jsonify([user.serialize() for user in users]), status_code


################   ENDPOINTS PARA PLANETAS ##################

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planets.query.get(id)
    status_code = 400 if planet is None else 200
    return jsonify(planet.serialize()), status_code

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    status_code = 400 if planets is None else 200
    return jsonify([planet.serialize() for planet in planets]), status_code

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"msg": "no hay usuario a quien agregar"})
    
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"msg": "planeta no existe"}), 404
    
    user_id = data["user_id"]
    user = User.query.get(user_id)   

    if user is None:
        return jsonify({"msg": "usuario no existe"}), 404
    else:
        user.favorite_planets.append(planet)
        db.session.commit()
        return jsonify({"msg": "agregado"}), 200 

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"msg": "no hay usuario a quien agregar"})
    
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"msg": "planeta no existe"}), 404
    
    user_id = data["user_id"]
    user = User.query.get(user_id)   

    if user is None:
        return jsonify({"msg": "usuario no existe"}), 404
    
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
        return jsonify({"msg": "planeta eliminado"})
    else:
        return jsonify({"msg": "el planeta no es favorito del usuario"})


@app.route('/planet', methods=['POST'])
def add_planet():
    data = request.get_json()

    required_fields = [
        "name", "description", "population", "climate",
        "gravity", "diameter", "orbital_period",
        "terrain", "rotation_period"
    ]

    # Validar que estén todos los campos
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Falta el campo requerido: {field}"}), 400

    try:
        # Crear nuevo planeta
        new_planet = Planets(
            name=data["name"],
            description=data["description"],
            population=data["population"],
            climate=data["climate"],
            gravity=data["gravity"],
            diameter=data["diameter"],
            orbital_period=data["orbital_period"],
            terrain=data["terrain"],
            rotation_period=data["rotation_period"]
        )

        db.session.add(new_planet)
        db.session.commit()

        return jsonify({"msg": "Planeta creado exitosamente", "planet": new_planet.serialize()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al crear el planeta", "error": str(e)}), 500


################   ENDPOINTS PARA ESPECIES ##################

@app.route('/species/<int:id>', methods=['GET'])
def get_species_by_id(id):
    species = Species.query.get(id)
    status_code = 400 if species is None else 200
    return jsonify(species.serialize()), status_code

@app.route('/species', methods=['GET'])
def get_all_species():
    species = Species.query.all()
    status_code = 400 if species is None else 200
    return jsonify([specie.serialize() for specie in species]), status_code

@app.route('/favorite/species/<int:species_id>', methods=['POST'])
def add_favorite_species(species_id):
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"msg": "es necesario proporcionar un user_id"})
    
    species = Species.query.get(species_id)

    if species is None:
        return jsonify({"msg": "especie no existe"}), 404
    
    user_id = data["user_id"]
    user = User.query.get(user_id)   

    if user is None:
        return jsonify({"msg": "usuario no existe"}), 404
    else:
        user.favorite_species.append(species)
        db.session.commit()
        return jsonify({"msg": "agregado"}), 200 

@app.route('/favorite/species/<int:species_id>', methods=['DELETE'])
def delete_favorite_species(species_id):
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"msg": "no hay usuario a quien agregar"})
    
    species = Species.query.get(species_id)

    if species is None:
        return jsonify({"msg": "species no existe"}), 404
    
    user_id = data["user_id"]
    user = User.query.get(user_id)   

    if user is None:
        return jsonify({"msg": "usuario no existe"}), 404
    
    if species in user.favorite_species:
        user.favorite_species.remove(species)
        db.session.commit()
        return jsonify({"msg": "species eliminado"})
    else:
        return jsonify({"msg": "la especie no es favorito del usuario"})

@app.route('/species', methods=['POST'])
def add_species():
    data = request.get_json()

    required_fields = [
        "name", "description", "classification", "language",
        "average_lifespan", "average_height", "designation",
        "eye_colors", "hair_colors"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Falta el campo requerido: {field}"}), 400

    try:
        new_species = Species(
            name=data["name"],
            description=data["description"],
            classification=data["classification"],
            language=data["language"],
            average_lifespan=data["average_lifespan"],
            average_height=data["average_height"],
            designation=data["designation"],
            eye_colors=data["eye_colors"],
            hair_colors=data["hair_colors"]
        )

        db.session.add(new_species)
        db.session.commit()

        return jsonify({
            "msg": "Especie creada exitosamente",
            "species": new_species.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "msg": "Error al crear la especie",
            "error": str(e)
        }), 500



################   ENDPOINTS PARA PERSONAS ##################

@app.route('/people/<int:id>', methods=['GET'])
def get_people_by_id(id):
    person = People.query.get(id)
    status_code = 400 if person is None else 200
    return jsonify(person.serialize()), status_code

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    status_code = 400 if people is None else 200
    return jsonify([person.serialize() for person in people]), status_code

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"msg": "es necesario proporcionar un user_id"})
    
    people = People.query.get(people_id)

    if people is None:
        return jsonify({"msg": "especie no existe"}), 404
    
    user_id = data["user_id"]
    user = User.query.get(user_id)   

    if user is None:
        return jsonify({"msg": "usuario no existe"}), 404
    else:
        user.favorite_people.append(people)
        db.session.commit()
        return jsonify({"msg": "agregado"}), 200 

@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_people(person_id):
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"msg": "no hay usuario a quien agregar"})
    
    person = People.query.get(person_id)

    if person is None:
        return jsonify({"msg": "person no existe"}), 404
    
    user_id = data["user_id"]
    user = User.query.get(user_id)   

    if user is None:
        return jsonify({"msg": "usuario no existe"}), 404
    
    if person in user.favorite_people:
        user.favorite_people.remove(person)
        db.session.commit()
        return jsonify({"msg": "person eliminado"})
    else:
        return jsonify({"msg": "person no es favorito del usuario"})
    

@app.route('/people', methods=['POST'])
def add_person():
    data = request.get_json()

    required_fields = [
        "name", "description", "height", "gender", "birth_year",
        "hair_color", "mass", "skin_color"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Falta el campo requerido: {field}"}), 400

    try:
        new_person = People(
            name=data["name"],
            description=data["description"],
            height=data["height"],
            gender=data["gender"],
            birth_year=data["birth_year"],
            hair_color=data["hair_color"],
            mass=data["mass"],
            skin_color=data["skin_color"]
        )

        db.session.add(new_person)
        db.session.commit()

        return jsonify({
            "msg": "Personaje creado exitosamente",
            "person": new_person.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "msg": "Error al crear la persona",
            "error": str(e)
        }), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
