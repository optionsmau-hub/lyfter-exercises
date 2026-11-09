"""
Seeds the database with fake data via Faker, inserting everything
through the manager classes (ORM) -- no raw SQL anywhere here.

Generates at least 20 users, each with 1-2 addresses and 0-2 cars, plus
a handful of extra cars with no owner at all.

Run from this folder:
    python seed_with_faker.py
"""

import hashlib
import random

from faker import Faker

from database import SessionLocal
from managers import AutomovilManager, DireccionManager, UsuarioManager
from models import Automovil, Direccion, Usuario

USER_COUNT = 25
UNOWNED_CAR_COUNT = 8

CAR_BRANDS_MODELS = [
    ("Toyota", "Corolla"), ("Honda", "Civic"), ("Ford", "Focus"), ("Chevrolet", "Malibu"),
    ("Nissan", "Sentra"), ("Hyundai", "Elantra"), ("Kia", "Sportage"), ("Mazda", "CX-5"),
    ("Volkswagen", "Jetta"), ("Subaru", "Outback"), ("BMW", "3 Series"), ("Mercedes-Benz", "C-Class"),
    ("Audi", "A4"), ("Jeep", "Wrangler"), ("Tesla", "Model 3"),
]

fake = Faker()
usuarios_mgr = UsuarioManager()
direcciones_mgr = DireccionManager()
automoviles_mgr = AutomovilManager()


def fake_password_hash():
    return hashlib.sha256(fake.password(length=12).encode()).hexdigest()


def reset_tables():
    # Bulk delete expressed through the ORM, not a raw SQL string.
    with SessionLocal() as session:
        session.query(Direccion).delete()
        session.query(Automovil).delete()
        session.query(Usuario).delete()
        session.commit()


def crear_auto_aleatorio(usuario_id=None):
    brand, model = random.choice(CAR_BRANDS_MODELS)
    automoviles_mgr.crear(
        marca=brand,
        modelo=model,
        anio=random.randint(2015, 2024),
        placa=fake.unique.license_plate(),
        usuario_id=usuario_id,
    )


def main():
    fake.unique.clear()

    print("Vaciando usuarios, direcciones y automoviles...")
    reset_tables()

    print(f"Generando {USER_COUNT} usuarios con direcciones y autos aleatorios...")
    for _ in range(USER_COUNT):
        usuario = usuarios_mgr.crear(
            nombre_completo=fake.name(),
            email=fake.unique.email(),
            username=fake.unique.user_name(),
            password=fake_password_hash(),
            fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=70),
        )

        for _ in range(random.randint(1, 2)):
            direcciones_mgr.crear(
                usuario_id=usuario.id,
                calle=fake.street_address(),
                ciudad=fake.city(),
                provincia=fake.state(),
                codigo_postal=fake.postcode(),
            )

        for _ in range(random.randint(0, 2)):
            crear_auto_aleatorio(usuario_id=usuario.id)

    print(f"Generando {UNOWNED_CAR_COUNT} automoviles sin usuario asignado...")
    for _ in range(UNOWNED_CAR_COUNT):
        crear_auto_aleatorio(usuario_id=None)

    total_usuarios = len(usuarios_mgr.consultar_todos())
    total_autos = len(automoviles_mgr.consultar_todos())
    total_direcciones = len(direcciones_mgr.consultar_todas())
    sin_usuario = len(automoviles_mgr.consultar_sin_usuario())

    print(
        f"Listo: usuarios={total_usuarios}, direcciones={total_direcciones}, "
        f"automoviles={total_autos} (sin usuario={sin_usuario})"
    )


if __name__ == "__main__":
    main()
