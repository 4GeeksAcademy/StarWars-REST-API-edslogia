from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Date, Time, DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(Integer(), nullable=False)
    nickname:Mapped[str] = mapped_column(String(16), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)  
    favorite_planet: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="user")
    favorite_species: Mapped[list["FavoriteSpecies"]] = relationship("FavoriteSpecies", back_populates="user")
    planet_people: Mapped[list["FavoritePeople"]] = relationship("FavoritePeople", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(Integer(),primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="favorite_planet")

class FavoriteSpecies(db.Model):
    id: Mapped[int] = mapped_column(Integer(),primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="favorite_species")

class FavoritePeople(db.Model):
    id: Mapped[int] = mapped_column(Integer(),primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="favorite_people")

try:
    render_er(db.Model, 'diagram.png')
    print("✅ Diagrama generado correctamente como diagram.png")
except Exception as e:
    print("❌ Error generando el diagrama:", e)