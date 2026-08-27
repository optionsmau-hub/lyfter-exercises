# Ejercicio Extra Diccionarios 2: Agrupar empleados por departamento
employees = [
    ("Alice", "alice@corp.com", "Engineering"),
    ("Bob", "bob@corp.com", "HR"),
    ("Carlos", "carlos@corp.com", "Engineering"),
    ("Diana", "diana@corp.com", "Marketing"),
    ("Eve", "eve@corp.com", "HR")
]

# group employees by department
by_dept = {}

for name, email, dept in employees:
    # create the department key if it doesn't exist
    if dept not in by_dept:
        by_dept[dept] = []
    # append the employee tuple (name, email)
    by_dept[dept].append((name, email))

# show the grouped result
for dept, staff in by_dept.items():
    print(f"{dept}: {staff}")