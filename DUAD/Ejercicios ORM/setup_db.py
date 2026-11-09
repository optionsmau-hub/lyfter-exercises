"""
Checks whether usuarios, direcciones and automoviles exist, and creates
whichever ones are missing. Uses SQLAlchemy's inspection API only --
no raw SQL.

Run from this folder:
    python setup_db.py
"""

from sqlalchemy import inspect

import models  # noqa: F401  (registers the models on Base.metadata)
from database import Base, engine

REQUIRED_TABLES = ["usuarios", "direcciones", "automoviles"]


def main():
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())

    missing = [table for table in REQUIRED_TABLES if table not in existing]
    if not missing:
        print("Las tablas ya existen: " + ", ".join(REQUIRED_TABLES))
        return

    print("Faltan tablas: " + ", ".join(missing) + ". Creandolas...")
    Base.metadata.create_all(engine)
    print("Listo. Tablas creadas: " + ", ".join(missing))


if __name__ == "__main__":
    main()
