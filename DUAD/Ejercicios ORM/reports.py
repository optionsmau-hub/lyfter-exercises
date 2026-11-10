"""
Uses the bidirectional relationships (user.cars, user.addresses) to
print everything a given user owns, in one query.
"""

from sqlalchemy.orm import selectinload

from database import SessionLocal
from models import User


def print_cars_and_addresses(user_id):
    with SessionLocal() as session:
        user = session.get(User, user_id, options=[selectinload(User.cars), selectinload(User.addresses)])
        if user is None:
            print(f"Usuario {user_id} no existe.")
            return

        print(f"Usuario: {user.full_name} (id={user.id})")

        print(f"Autos ({len(user.cars)}):")
        for car in user.cars:
            print(f"  - {car.brand} {car.model} ({car.year}) placa={car.license_plate}")

        print(f"Direcciones ({len(user.addresses)}):")
        for address in user.addresses:
            print(f"  - {address.street}, {address.city}, {address.province}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python reports.py <user_id>")
        sys.exit(1)

    print_cars_and_addresses(int(sys.argv[1]))
