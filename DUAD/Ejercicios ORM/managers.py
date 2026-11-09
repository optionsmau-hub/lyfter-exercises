"""
Manager classes: one per entity, each wrapping a short-lived SQLAlchemy
session per call. All data access goes through the ORM (session.get,
session.scalars, etc.) -- no raw SQL anywhere in this file.
"""

from sqlalchemy import select

from database import SessionLocal
from models import Automovil, Direccion, Usuario


class UsuarioManager:
    def crear(self, nombre_completo, email, username, password, fecha_nacimiento, estado="activo"):
        with SessionLocal() as session:
            usuario = Usuario(
                nombre_completo=nombre_completo,
                email=email,
                username=username,
                password=password,
                fecha_nacimiento=fecha_nacimiento,
                estado=estado,
            )
            session.add(usuario)
            session.commit()
            return usuario

    def modificar(self, usuario_id, **campos):
        with SessionLocal() as session:
            usuario = session.get(Usuario, usuario_id)
            if usuario is None:
                return None
            for campo, valor in campos.items():
                setattr(usuario, campo, valor)
            session.commit()
            return usuario

    def eliminar(self, usuario_id):
        with SessionLocal() as session:
            usuario = session.get(Usuario, usuario_id)
            if usuario is None:
                return False
            session.delete(usuario)
            session.commit()
            return True

    def consultar_todos(self):
        with SessionLocal() as session:
            return list(session.scalars(select(Usuario)).all())


class AutomovilManager:
    def crear(self, marca, modelo, anio, placa, usuario_id=None):
        with SessionLocal() as session:
            automovil = Automovil(marca=marca, modelo=modelo, anio=anio, placa=placa, usuario_id=usuario_id)
            session.add(automovil)
            session.commit()
            return automovil

    def modificar(self, automovil_id, **campos):
        with SessionLocal() as session:
            automovil = session.get(Automovil, automovil_id)
            if automovil is None:
                return None
            for campo, valor in campos.items():
                setattr(automovil, campo, valor)
            session.commit()
            return automovil

    def eliminar(self, automovil_id):
        with SessionLocal() as session:
            automovil = session.get(Automovil, automovil_id)
            if automovil is None:
                return False
            session.delete(automovil)
            session.commit()
            return True

    def asociar_usuario(self, automovil_id, usuario_id):
        with SessionLocal() as session:
            automovil = session.get(Automovil, automovil_id)
            if automovil is None:
                raise LookupError(f"Automovil {automovil_id} no existe.")
            if session.get(Usuario, usuario_id) is None:
                raise LookupError(f"Usuario {usuario_id} no existe.")
            automovil.usuario_id = usuario_id
            session.commit()
            return automovil

    def consultar_todos(self):
        with SessionLocal() as session:
            return list(session.scalars(select(Automovil)).all())


class DireccionManager:
    def crear(self, usuario_id, calle, ciudad, provincia, codigo_postal):
        with SessionLocal() as session:
            if session.get(Usuario, usuario_id) is None:
                raise LookupError(f"Usuario {usuario_id} no existe.")
            direccion = Direccion(
                usuario_id=usuario_id, calle=calle, ciudad=ciudad, provincia=provincia, codigo_postal=codigo_postal
            )
            session.add(direccion)
            session.commit()
            return direccion

    def modificar(self, direccion_id, **campos):
        with SessionLocal() as session:
            direccion = session.get(Direccion, direccion_id)
            if direccion is None:
                return None
            for campo, valor in campos.items():
                setattr(direccion, campo, valor)
            session.commit()
            return direccion

    def eliminar(self, direccion_id):
        with SessionLocal() as session:
            direccion = session.get(Direccion, direccion_id)
            if direccion is None:
                return False
            session.delete(direccion)
            session.commit()
            return True

    def consultar_todas(self):
        with SessionLocal() as session:
            return list(session.scalars(select(Direccion)).all())
