"""
Resets users, cars and rentals and repopulates them with fake data via
Faker: 200 users, 100 cars, and a random number of rentals (50-150)
simulating rental history.

Car brand/model pairs come from a small curated pool (Faker has no
built-in vehicle provider) but are picked, like everything else here,
through the shared Faker instance.

Run from anywhere:
    python scripts/seed_with_faker.py
"""

import os
import random
import sys
from datetime import timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "api"))

import psycopg2.extras
from faker import Faker
from werkzeug.security import generate_password_hash

from db import get_connection

USER_COUNT = 200
CAR_COUNT = 100
MIN_RENTALS = 50
MAX_RENTALS = 150

USER_STATUSES = ["active", "active", "active", "active", "inactive", "suspended", "delinquent"]
CAR_STATUSES = ["available", "available", "available", "available", "rented", "maintenance"]
RENTAL_STATUSES = ["active", "completed", "completed", "completed", "cancelled"]

CAR_BRANDS_MODELS = [
    ("Toyota", "Corolla"), ("Honda", "Civic"), ("Ford", "Focus"), ("Chevrolet", "Malibu"),
    ("Nissan", "Sentra"), ("Hyundai", "Elantra"), ("Kia", "Sportage"), ("Mazda", "CX-5"),
    ("Volkswagen", "Jetta"), ("Subaru", "Outback"), ("BMW", "3 Series"), ("Mercedes-Benz", "C-Class"),
    ("Audi", "A4"), ("Jeep", "Wrangler"), ("Tesla", "Model 3"),
]

fake = Faker()


def reset_tables(cur):
    cur.execute("TRUNCATE TABLE rentals, cars, users RESTART IDENTITY CASCADE")


def seed_users(cur, count):
    fake.unique.clear()
    rows = [
        (
            fake.name(),
            fake.unique.email(),
            fake.unique.user_name(),
            generate_password_hash(fake.password(length=12)),
            fake.date_of_birth(minimum_age=18, maximum_age=70),
            fake.random_element(USER_STATUSES),
        )
        for _ in range(count)
    ]
    psycopg2.extras.execute_values(
        cur, "INSERT INTO users (full_name, email, username, password, birth_date, status) VALUES %s", rows
    )


def seed_cars(cur, count):
    rows = []
    for _ in range(count):
        brand, model = fake.random_element(CAR_BRANDS_MODELS)
        rows.append((brand, model, fake.random_int(min=2015, max=2024), fake.random_element(CAR_STATUSES)))
    psycopg2.extras.execute_values(cur, "INSERT INTO cars (brand, model, year, status) VALUES %s", rows)


def seed_rentals(cur, user_ids, car_ids, count):
    rows = []
    for _ in range(count):
        status = fake.random_element(RENTAL_STATUSES)
        rental_date = fake.date_time_between(start_date="-1y", end_date="now")
        return_date = (
            rental_date + timedelta(hours=fake.random_int(min=2, max=240))
            if status in ("completed", "cancelled")
            else None
        )
        rows.append((fake.random_element(user_ids), fake.random_element(car_ids), rental_date, return_date, status))

    psycopg2.extras.execute_values(
        cur, "INSERT INTO rentals (user_id, car_id, rental_date, return_date, status) VALUES %s", rows
    )

    # Keep each car's own status consistent with having an active rental,
    # the same invariant the API maintains (skip cars taken offline on purpose).
    cur.execute(
        """
        UPDATE cars SET status = 'rented'
        WHERE status != 'disabled'
          AND id IN (SELECT car_id FROM rentals WHERE status = 'active')
        """
    )


def main():
    rental_count = random.randint(MIN_RENTALS, MAX_RENTALS)

    with get_connection() as conn:
        with conn.cursor() as cur:
            print("Vaciando users, cars y rentals...")
            reset_tables(cur)

            print(f"Generando {USER_COUNT} usuarios con Faker...")
            seed_users(cur, USER_COUNT)

            print(f"Generando {CAR_COUNT} automoviles con Faker...")
            seed_cars(cur, CAR_COUNT)

            cur.execute("SELECT id FROM users")
            user_ids = [row[0] for row in cur.fetchall()]
            cur.execute("SELECT id FROM cars")
            car_ids = [row[0] for row in cur.fetchall()]

            print(f"Generando {rental_count} alquileres con Faker...")
            seed_rentals(cur, user_ids, car_ids, rental_count)

    print(f"Listo: users={USER_COUNT}, cars={CAR_COUNT}, rentals={rental_count}")


if __name__ == "__main__":
    main()
