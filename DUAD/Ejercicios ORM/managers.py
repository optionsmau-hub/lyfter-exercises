"""
Manager classes: one per entity, each wrapping a short-lived SQLAlchemy
session per call. All data access goes through the ORM (session.get,
session.scalars, etc.) -- no raw SQL anywhere in this file.
"""

from sqlalchemy import func, select

from database import SessionLocal
from models import Address, Car, User


class UserManager:
    def create(self, full_name, email, username, password, birth_date, status="active"):
        with SessionLocal() as session:
            user = User(
                full_name=full_name,
                email=email,
                username=username,
                password=password,
                birth_date=birth_date,
                status=status,
            )
            session.add(user)
            session.commit()
            return user

    def update(self, user_id, **fields):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if user is None:
                return None
            for field, value in fields.items():
                setattr(user, field, value)
            session.commit()
            return user

    def delete(self, user_id):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if user is None:
                return False
            session.delete(user)
            session.commit()
            return True

    def get_all(self):
        with SessionLocal() as session:
            return list(session.scalars(select(User)).all())

    def get_with_more_than_one_car(self):
        """Users with more than 1 car associated."""
        with SessionLocal() as session:
            stmt = (
                select(User)
                .join(Car, Car.user_id == User.id)
                .group_by(User.id)
                .having(func.count(Car.id) > 1)
            )
            return list(session.scalars(stmt).all())


class CarManager:
    def create(self, brand, model, year, license_plate, user_id=None):
        with SessionLocal() as session:
            car = Car(brand=brand, model=model, year=year, license_plate=license_plate, user_id=user_id)
            session.add(car)
            session.commit()
            return car

    def update(self, car_id, **fields):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if car is None:
                return None
            for field, value in fields.items():
                setattr(car, field, value)
            session.commit()
            return car

    def delete(self, car_id):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if car is None:
                return False
            session.delete(car)
            session.commit()
            return True

    def assign_user(self, car_id, user_id):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if car is None:
                raise LookupError(f"Car {car_id} does not exist.")
            if session.get(User, user_id) is None:
                raise LookupError(f"User {user_id} does not exist.")
            car.user_id = user_id
            session.commit()
            return car

    def get_all(self):
        with SessionLocal() as session:
            return list(session.scalars(select(Car)).all())

    def get_without_user(self):
        """Cars with no user associated."""
        with SessionLocal() as session:
            stmt = select(Car).where(Car.user_id.is_(None))
            return list(session.scalars(stmt).all())


class AddressManager:
    def create(self, user_id, street, city, province, postal_code):
        with SessionLocal() as session:
            if session.get(User, user_id) is None:
                raise LookupError(f"User {user_id} does not exist.")
            address = Address(user_id=user_id, street=street, city=city, province=province, postal_code=postal_code)
            session.add(address)
            session.commit()
            return address

    def update(self, address_id, **fields):
        with SessionLocal() as session:
            address = session.get(Address, address_id)
            if address is None:
                return None
            for field, value in fields.items():
                setattr(address, field, value)
            session.commit()
            return address

    def delete(self, address_id):
        with SessionLocal() as session:
            address = session.get(Address, address_id)
            if address is None:
                return False
            session.delete(address)
            session.commit()
            return True

    def get_all(self):
        with SessionLocal() as session:
            return list(session.scalars(select(Address)).all())

    def search_by_street(self, substring):
        """Addresses whose street contains the given substring (case-insensitive)."""
        with SessionLocal() as session:
            stmt = select(Address).where(Address.street.ilike(f"%{substring}%"))
            return list(session.scalars(stmt).all())
