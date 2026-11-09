"""
ORM models: Usuario, Direccion and Automovil.

- Direccion.usuario_id is NOT NULL: every address must belong to a user.
- Automovil.usuario_id is nullable: a car can exist without an owner.
"""

from datetime import date
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="activo")

    direcciones: Mapped[List["Direccion"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )
    automoviles: Mapped[List["Automovil"]] = relationship(back_populates="usuario")

    def __repr__(self):
        return f"<Usuario id={self.id} username={self.username!r}>"


class Direccion(Base):
    __tablename__ = "direcciones"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    calle: Mapped[str] = mapped_column(String(150), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(80), nullable=False)
    provincia: Mapped[str] = mapped_column(String(80), nullable=False)
    codigo_postal: Mapped[str] = mapped_column(String(20), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="direcciones")

    def __repr__(self):
        return f"<Direccion id={self.id} usuario_id={self.usuario_id}>"


class Automovil(Base):
    __tablename__ = "automoviles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    marca: Mapped[str] = mapped_column(String(60), nullable=False)
    modelo: Mapped[str] = mapped_column(String(60), nullable=False)
    anio: Mapped[int] = mapped_column(nullable=False)
    placa: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    usuario: Mapped[Optional["Usuario"]] = relationship(back_populates="automoviles")

    def __repr__(self):
        return f"<Automovil id={self.id} placa={self.placa!r} usuario_id={self.usuario_id}>"
