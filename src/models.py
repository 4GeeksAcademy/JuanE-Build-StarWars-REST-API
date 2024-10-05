from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.email,
            "last": self.last,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    gender = db.Column(db.String(250), nullable=False)

    
    def __repr__(self):
        return '<Get people %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "birth_year": self.birth_year,
            "hair_color": self.hair_color,
            "gender": self.gender,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return '<Get planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
        
            # do not serialize the password, its a security breach
        }
    
class Favorite(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id= db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship((User))
    planet = db.relationship((Planet))
    character = db.relationship((People))

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet.serialize() if self.planet else None,
            "character" : self.character.serialize() if self.character else None,
            "user" : self.user.serialize(),
            
        
            # do not serialize the password, its a security breach
        }