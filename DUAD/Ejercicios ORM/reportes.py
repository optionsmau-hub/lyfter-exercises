"""
Uses the bidirectional relationships (usuario.autos, usuario.direcciones)
to print everything a given user owns, in one query.
"""

from sqlalchemy.orm import selectinload

from database import SessionLocal
from models import Usuario


def imprimir_autos_y_direcciones(usuario_id):
    with SessionLocal() as session:
        usuario = session.get(
            Usuario, usuario_id, options=[selectinload(Usuario.autos), selectinload(Usuario.direcciones)]
        )
        if usuario is None:
            print(f"Usuario {usuario_id} no existe.")
            return

        print(f"Usuario: {usuario.nombre_completo} (id={usuario.id})")

        print(f"Autos ({len(usuario.autos)}):")
        for auto in usuario.autos:
            print(f"  - {auto.marca} {auto.modelo} ({auto.anio}) placa={auto.placa}")

        print(f"Direcciones ({len(usuario.direcciones)}):")
        for direccion in usuario.direcciones:
            print(f"  - {direccion.calle}, {direccion.ciudad}, {direccion.provincia}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python reportes.py <usuario_id>")
        sys.exit(1)

    imprimir_autos_y_direcciones(int(sys.argv[1]))
