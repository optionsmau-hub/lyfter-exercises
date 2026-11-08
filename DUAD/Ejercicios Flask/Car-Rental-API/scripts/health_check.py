"""
Checks that the database is reachable, that users/cars/rentals exist,
and that there is at least one available car.

Exit code is 0 on success, 1 on any failure (connection, missing
tables, or no available cars), so this can also be used from CI or a
monitoring job, not just read by a human.

Run from anywhere:
    python scripts/health_check.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "api"))

import psycopg2

from db import get_connection

SCHEMA = "lyfter_car_rental"
REQUIRED_TABLES = ["users", "cars", "rentals"]


def main():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                missing_tables = []
                for table in REQUIRED_TABLES:
                    cur.execute(
                        """
                        SELECT EXISTS (
                            SELECT 1 FROM information_schema.tables
                            WHERE table_schema = %s AND table_name = %s
                        )
                        """,
                        (SCHEMA, table),
                    )
                    if not cur.fetchone()[0]:
                        missing_tables.append(table)

                if missing_tables:
                    print(f"DB ERROR. Faltan tablas: {', '.join(missing_tables)}")
                    return 1

                cur.execute("SELECT COUNT(*) FROM cars WHERE status = 'available'")
                available_cars = cur.fetchone()[0]
                if available_cars < 1:
                    print("DB ERROR. No hay autos disponibles")
                    return 1

    except psycopg2.OperationalError as error:
        print(f"DB ERROR. No se pudo conectar a la base de datos: {error}")
        return 1

    print("DB OK. Sistema operativo con normalidad")
    return 0


if __name__ == "__main__":
    sys.exit(main())
