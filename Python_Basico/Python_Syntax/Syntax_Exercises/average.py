# Programa para calcular estadísticas de notas de un estudiante

total_de_notas = int(input("Ingrese la cantidad de notas: "))

contador_de_nota = 1
cantidad_de_notas_aprobadas = 0
cantidad_de_notas_desaprobadas = 0
suma_notas_aprobadas = 0
suma_notas_desaprobadas = 0
suma_total = 0

while contador_de_nota <= total_de_notas:
    nota_actual = float(input(f"Ingrese la nota número {contador_de_nota}: "))

    if nota_actual < 70:
        cantidad_de_notas_desaprobadas += 1
        suma_notas_desaprobadas += nota_actual
    else:
        cantidad_de_notas_aprobadas += 1
        suma_notas_aprobadas += nota_actual

    suma_total += nota_actual
    contador_de_nota += 1

# Cálculo de promedios
promedio_total = suma_total / total_de_notas

if cantidad_de_notas_aprobadas > 0:
    promedio_aprobadas = suma_notas_aprobadas / cantidad_de_notas_aprobadas
else:
    promedio_aprobadas = 0

if cantidad_de_notas_desaprobadas > 0:
    promedio_desaprobadas = suma_notas_desaprobadas / cantidad_de_notas_desaprobadas
else:
    promedio_desaprobadas = 0

# Resultados
print("Cantidad de notas aprobadas:", cantidad_de_notas_aprobadas)
print("Promedio de notas aprobadas:", promedio_aprobadas)

print("Cantidad de notas desaprobadas:", cantidad_de_notas_desaprobadas)
print("Promedio de notas desaprobadas:", promedio_desaprobadas)

print("Promedio total de notas:", promedio_total)
