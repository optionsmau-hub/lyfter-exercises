# Ejercicios de ORMs (SQLAlchemy)

Todo el acceso a datos pasa por SQLAlchemy; no hay SQL escrito a mano en ningún script de este proyecto.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # y edita .env con tus credenciales de Postgres
```

**Tarea 1 — versión de SQLAlchemy** (toma el screenshot de esta salida para la entrega):
```bash
python check_sqlalchemy_version.py
```

## Modelos (Tarea 2)

`models.py` define `User`, `Address` y `Car`:
- `addresses.user_id` es **NOT NULL** (toda dirección necesita un usuario).
- `cars.user_id` es **nullable** (un auto puede no tener dueño).
- Ambas tienen FK a `users`.

## Crear las tablas (Tarea 3)

```bash
python setup_db.py
```
Revisa qué tablas existen (vía `sqlalchemy.inspect`, sin SQL) y crea solo las que faltan. Se puede correr las veces que sea — si ya existen, lo dice y no hace nada.

## Clases manager (Tarea 4)

`managers.py` tiene `UserManager`, `CarManager` y `AddressManager`, cada una con `create`, `update`, `delete` y el `get_all` correspondiente. `CarManager.assign_user(car_id, user_id)` asocia un auto existente a un usuario existente.

## Ver todo funcionando junto

```bash
python demo.py
```
Crea un usuario, un auto sin dueño, lo asocia al usuario, crea una dirección, prueba que una dirección con un usuario inexistente se rechaza, consulta todos los registros, y al final borra lo que creó (se puede correr varias veces sin dejar basura).

## Extra: filtros avanzados (Tarea 1 extra)

- `CarManager.get_without_user()` — autos sin usuario asociado.
- `UserManager.get_with_more_than_one_car()` — usuarios con más de 1 auto.
- `AddressManager.search_by_street(substring)` — direcciones cuya calle contiene ese substring (sin distinguir mayúsculas/minúsculas).

## Extra: relaciones bidireccionales (Tarea 2 extra)

`user.cars` y `user.addresses` dan acceso directo a los autos/direcciones de ese usuario. `reports.py` los usa para imprimir todo lo de un usuario dado su id:

```bash
python reports.py <user_id>
```

## Extra: seed con Faker (Tarea 3 extra)

```bash
python seed_with_faker.py
```
Vacía y repuebla la base con 25 usuarios (cada uno con 1-2 direcciones y 0-2 autos) más 8 autos sin usuario asignado — todo insertado a través de `UserManager`, `AddressManager` y `CarManager` (ORM puro, sin SQL).
