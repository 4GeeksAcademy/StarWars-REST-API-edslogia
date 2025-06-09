from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Date, Time, DateTime, Integer, Numeric, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er
from datetime import datetime

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
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(Integer(), nullable=False)
    nickname:Mapped[str] = mapped_column(String(16), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)  
    favorite_planets: Mapped[list["Planets"]] = relationship("Planets", secondary=user_planet_favorites, back_populates="fans")
    favorite_species: Mapped[list["Species"]] = relationship("Species", secondary=user_species_favorites, back_populates="fans")
    favorite_people: Mapped[list["People"]] = relationship("People", secondary=user_people_favorites, back_populates="fans")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,            
            "nickname": self.nickname,
            "favorite_planet" : self.favorite_planet,
            "favorite_species" : self.favorite_species,
            "favorite_people" : self.favorite_people
        }

class Planets(db.Model):
    id: Mapped[int] = mapped_column(Integer(),primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str] = mapped_column(String(80), nullable=False)
    diameter_km: Mapped[float] = mapped_column(Numeric(20,2), nullable=False)
    population: Mapped[int] = mapped_column(Integer(), nullable=False)
    terrain: Mapped[str] = mapped_column(String(80), nullable=False)
    fans: Mapped[list["User"]] = relationship("User", secondary=user_planet_favorites, back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter_km": self.diameter_km,
            "population": self.population,
            "terrain": self.terrain
        }  

class Species(db.Model):
    id: Mapped[int] = mapped_column(Integer(),primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    average_height: Mapped[float] = mapped_column(Numeric(3,2), nullable=False)
    classification: Mapped[str] = mapped_column(String(80), nullable=False)
    language: Mapped[str] = mapped_column(String(80), nullable=False)
    skin_colors: Mapped[str] = mapped_column(String(80), nullable=False)
    fans: Mapped[list["User"]] = relationship("User", secondary=user_species_favorites, back_populates="favorite_species")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "average_height": self.average_height,
            "classification": self.classification,
            "language": self.language,
            "homeworld": self.homeworld
        }  
    
class People(db.Model):
    id: Mapped[int] = mapped_column(Integer(),primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(80), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(80), nullable=False)
    gender: Mapped[str] = mapped_column(String(80), nullable= True)
    height_cm: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    fans: Mapped[list["User"]] = relationship("User", secondary=user_people_favorites, back_populates="favorite_people")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "height_cm": self.height_cm
        }  


try:
    render_er(db.Model, 'diagram.png')
    print("✅ Diagrama generado correctamente como diagram.png")
except Exception as e:
    print("❌ Error generando el diagrama:", e)