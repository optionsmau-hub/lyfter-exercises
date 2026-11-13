"""
Exercises every manager method end to end, so it's easy to see (and
prove) that the ORM setup, the FKs and the CRUD methods all work
together. Safe to run more than once: cleans up what it creates at
the end.

Run from this folder:
    python demo.py
"""

from datetime import date

from managers import AddressManager, CarManager, UserManager

users = UserManager()
cars = CarManager()
addresses = AddressManager()


def main():
    print("--- Crear usuario ---")
    user = users.create(
        full_name="Ana Rodriguez",
        email="ana.demo@example.com",
        username="anademo",
        password="hash-de-ejemplo",
        birth_date=date(1992, 4, 15),
    )
    print(user)

    print("\n--- Modificar usuario ---")
    user = users.update(user.id, status="inactive")
    print(user, "status:", user.status)

    print("\n--- Crear automovil SIN usuario (debe ser valido) ---")
    car_without_owner = cars.create(brand="Toyota", model="Corolla", year=2022, license_plate="DEMO-001")
    print(car_without_owner, "user_id:", car_without_owner.user_id)

    print("\n--- Asociar ese automovil al usuario ---")
    car_without_owner = cars.assign_user(car_without_owner.id, user.id)
    print(car_without_owner, "user_id:", car_without_owner.user_id)

    print("\n--- Crear direccion (requiere usuario) ---")
    address = addresses.create(
        user_id=user.id, street="Calle 5", city="San Jose", province="San Jose", postal_code="10101"
    )
    print(address)

    print("\n--- Intentar crear direccion con usuario inexistente (debe fallar) ---")
    try:
        addresses.create(user_id=999999, street="X", city="X", province="X", postal_code="00000")
    except LookupError as error:
        print("Rechazado correctamente:", error)

    print("\n--- Consultar todos ---")
    print(f"usuarios: {len(users.get_all())}")
    print(f"automoviles: {len(cars.get_all())}")
    print(f"direcciones: {len(addresses.get_all())}")

    print("\n--- Limpieza ---")
    addresses.delete(address.id)
    cars.delete(car_without_owner.id)
    users.delete(user.id)
    print("Datos de la demo eliminados.")


if __name__ == "__main__":
    main()
