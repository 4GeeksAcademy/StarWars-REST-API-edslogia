from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Numeric, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_planet_favorites = Table(
    "user_planet_favorites",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planets.id"), primary_key=True)
)

user_species_favorites = Table(
    "user_species_favorites",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("species_id", ForeignKey("species.id"), primary_key=True)
)

user_people_favorites = Table(
    "user_people_favorites",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("person_id", ForeignKey("people.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)  
    favorite_planets: Mapped[list["Planets"]] = relationship("Planets", secondary=user_planet_favorites, back_populates="fans")
    favorite_species: Mapped[list["Species"]] = relationship("Species", secondary=user_species_favorites, back_populates="fans")
    favorite_people: Mapped[list["People"]] = relationship("People", secondary=user_people_favorites, back_populates="fans")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,       
            "age": self.age,
            "description": self.description,
            "nickname": self.nickname,
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets],
            "favorite_species": [specie.serialize() for specie in self.favorite_species],
            "favorite_people": [person.serialize() for person in self.favorite_people]
        }
    
    def serialize_favorites(self):
        return{
            "id": self.id,
            "email": self.email,    
            "nickname": self.nickname,
        }
    
    
class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    skin_color: Mapped[str] = mapped_column(nullable=False)
    fans: Mapped[list["User"]] = relationship("User", secondary=user_people_favorites, back_populates="favorite_people")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "height": self.height,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "hair_color": self.hair_color,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "fans": [fan.serialize_favorites() for fan in self.fans]            
        }  

class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    gravity: Mapped[int] = mapped_column(nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    orbital_period: Mapped[int] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    rotation_period: Mapped[int] = mapped_column(nullable=False)
    fans: Mapped[list["User"]] = relationship("User", secondary=user_planet_favorites, back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "population": self.population,
            "climate": self.climate,
            "gravity": self.gravity,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "terrain": self.terrain,
            "rotation_period": self.rotation_period,
            "fans": [fan.serialize_favorites() for fan in self.fans],
        }  

class Species(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    classification: Mapped[str] = mapped_column(nullable=False)
    language: Mapped[str] = mapped_column(nullable=False)
    average_lifespan: Mapped[int] = mapped_column(nullable=False)
    average_height: Mapped[int] = mapped_column(nullable=False)
    designation: Mapped[str] = mapped_column(nullable=False)
    eye_colors: Mapped[str] = mapped_column(nullable=False)
    hair_colors: Mapped[str] = mapped_column(nullable=False)
    fans: Mapped[list["User"]] = relationship("User", secondary=user_species_favorites, back_populates="favorite_species")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "classification": self.classification,
            "language": self.language,
            "average_lifespan": self.average_lifespan,
            "average_height": self.average_height,
            "designation": self.designation,
            "eye_colors": self.eye_colors,
            "hair_colors": self.hair_colors,
            "fans": [fan.serialize_favorites() for fan in self.fans],
        }  
    