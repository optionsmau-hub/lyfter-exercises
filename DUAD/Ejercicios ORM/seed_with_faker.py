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
from managers import AddressManager, CarManager, UserManager
from models import Address, Car, User

USER_COUNT = 25
UNOWNED_CAR_COUNT = 8

CAR_BRANDS_MODELS = [
    ("Toyota", "Corolla"), ("Honda", "Civic"), ("Ford", "Focus"), ("Chevrolet", "Malibu"),
    ("Nissan", "Sentra"), ("Hyundai", "Elantra"), ("Kia", "Sportage"), ("Mazda", "CX-5"),
    ("Volkswagen", "Jetta"), ("Subaru", "Outback"), ("BMW", "3 Series"), ("Mercedes-Benz", "C-Class"),
    ("Audi", "A4"), ("Jeep", "Wrangler"), ("Tesla", "Model 3"),
]

fake = Faker()
user_manager = UserManager()
address_manager = AddressManager()
car_manager = CarManager()


def fake_password_hash():
    return hashlib.sha256(fake.password(length=12).encode()).hexdigest()


def reset_tables():
    # Bulk delete expressed through the ORM, not a raw SQL string.
    with SessionLocal() as session:
        session.query(Address).delete()
        session.query(Car).delete()
        session.query(User).delete()
        session.commit()


def create_random_car(user_id=None):
    brand, model = random.choice(CAR_BRANDS_MODELS)
    car_manager.create(
        brand=brand,
        model=model,
        year=random.randint(2015, 2024),
        license_plate=fake.unique.license_plate(),
        user_id=user_id,
    )


def main():
    fake.unique.clear()

    print("Vaciando usuarios, direcciones y automoviles...")
    reset_tables()

    print(f"Generando {USER_COUNT} usuarios con direcciones y autos aleatorios...")
    for _ in range(USER_COUNT):
        user = user_manager.create(
            full_name=fake.name(),
            email=fake.unique.email(),
            username=fake.unique.user_name(),
            password=fake_password_hash(),
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=70),
        )

        for _ in range(random.randint(1, 2)):
            address_manager.create(
                user_id=user.id,
                street=fake.street_address(),
                city=fake.city(),
                province=fake.state(),
                postal_code=fake.postcode(),
            )

        for _ in range(random.randint(0, 2)):
            create_random_car(user_id=user.id)

    print(f"Generando {UNOWNED_CAR_COUNT} automoviles sin usuario asignado...")
    for _ in range(UNOWNED_CAR_COUNT):
        create_random_car(user_id=None)

    total_users = len(user_manager.get_all())
    total_cars = len(car_manager.get_all())
    total_addresses = len(address_manager.get_all())
    unowned = len(car_manager.get_without_user())

    print(
        f"Listo: usuarios={total_users}, direcciones={total_addresses}, "
        f"automoviles={total_cars} (sin usuario={unowned})"
    )


if __name__ == "__main__":
    main()
