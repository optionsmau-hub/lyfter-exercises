# Car Rental API

API REST para una empresa de alquiler de autos (Flask + PostgreSQL).

## 1. Base de datos

Con PostgreSQL corriendo y accesible, ejecuta estos scripts en orden (crean el schema, las tablas y las pueblan):

```bash
psql -U postgres -h localhost -d postgres -f sql/01_create_schema.sql
psql -U postgres -h localhost -d postgres -f sql/02_create_and_populate_users.sql
psql -U postgres -h localhost -d postgres -f sql/03_create_and_populate_cars.sql
psql -U postgres -h localhost -d postgres -f sql/04_create_rentals_table.sql
```

Deja 50 usuarios y 30 autos listos. Los scripts `sql/05` a `sql/13` prueban cada operación individual (agregar usuario/auto, cambiar estados, crear/completar alquiler, deshabilitar auto, listar autos alquilados/disponibles) — se corren igual, uno por uno, con `psql -f`.

## 2. API

```bash
cd api
pip install -r requirements.txt
cp .env.example .env   # y edita .env con tus credenciales de Postgres
python app.py
```

Queda en `http://127.0.0.1:5000`. Endpoints: `GET/POST /users`, `GET/POST /cars`, `GET/POST /rentals`, `PATCH /users/<id>/status`, `PATCH /users/<id>/flag-delinquent`, `PATCH /cars/<id>/status`, `PATCH /cars/<id>/disable`, `PATCH /rentals/<id>/complete`, `PATCH /rentals/<id>/status`. Los tres listados (`GET`) aceptan filtros por cualquier columna como query param, p. ej. `GET /cars?status=available`.

## 3. Scripts extra (desde la raíz del proyecto, con el `.env` de `api/` ya configurado)

**Chequeo de salud de la base:**
```bash
python scripts/health_check.py
```
Imprime `DB OK. Sistema operativo con normalidad` (exit code 0) o un mensaje `DB ERROR. ...` (exit code 1) si falla la conexión, faltan tablas, o no hay autos disponibles.

**Backup a CSV:**
```bash
python scripts/backup.py
```
Genera `db_backups/backup_<fecha>_users.csv`, `..._cars.csv` y `..._rentals.csv` con el contenido completo de cada tabla.

**Seed con datos falsos (Faker):**
```bash
python scripts/seed_with_faker.py
```
Vacía y repuebla la base con 200 usuarios, 100 autos y entre 50 y 150 alquileres históricos generados con Faker. Si quieres volver al seed original de 50/30 después, vuelve a correr los scripts `sql/02`, `sql/03` y `sql/04` del paso 1.
