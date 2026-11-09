"""
Exercises every manager method end to end, so it's easy to see (and
prove) that the ORM setup, the FKs and the CRUD methods all work
together. Safe to run more than once: cleans up what it creates at
the end.

Run from this folder:
    python demo.py
"""

from datetime import date

from managers import AutomovilManager, DireccionManager, UsuarioManager

usuarios = UsuarioManager()
automoviles = AutomovilManager()
direcciones = DireccionManager()


def main():
    print("--- Crear usuario ---")
    usuario = usuarios.crear(
        nombre_completo="Ana Rodriguez",
        email="ana.demo@example.com",
        username="anademo",
        password="hash-de-ejemplo",
        fecha_nacimiento=date(1992, 4, 15),
    )
    print(usuario)

    print("\n--- Modificar usuario ---")
    usuario = usuarios.modificar(usuario.id, estado="inactivo")
    print(usuario, "estado:", usuario.estado)

    print("\n--- Crear automovil SIN usuario (debe ser valido) ---")
    auto_sin_dueno = automoviles.crear(marca="Toyota", modelo="Corolla", anio=2022, placa="DEMO-001")
    print(auto_sin_dueno, "usuario_id:", auto_sin_dueno.usuario_id)

    print("\n--- Asociar ese automovil al usuario ---")
    auto_sin_dueno = automoviles.asociar_usuario(auto_sin_dueno.id, usuario.id)
    print(auto_sin_dueno, "usuario_id:", auto_sin_dueno.usuario_id)

    print("\n--- Crear direccion (requiere usuario) ---")
    direccion = direcciones.crear(
        usuario_id=usuario.id, calle="Calle 5", ciudad="San Jose", provincia="San Jose", codigo_postal="10101"
    )
    print(direccion)

    print("\n--- Intentar crear direccion con usuario inexistente (debe fallar) ---")
    try:
        direcciones.crear(usuario_id=999999, calle="X", ciudad="X", provincia="X", codigo_postal="00000")
    except LookupError as error:
        print("Rechazado correctamente:", error)

    print("\n--- Consultar todos ---")
    print(f"usuarios: {len(usuarios.consultar_todos())}")
    print(f"automoviles: {len(automoviles.consultar_todos())}")
    print(f"direcciones: {len(direcciones.consultar_todas())}")

    print("\n--- Limpieza ---")
    direcciones.eliminar(direccion.id)
    automoviles.eliminar(auto_sin_dueno.id)
    usuarios.eliminar(usuario.id)
    print("Datos de la demo eliminados.")


if __name__ == "__main__":
    main()
