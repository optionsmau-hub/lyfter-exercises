#data.py
# This file can be used to store any data-related functions or constants
# For now, it is left empty as no specific data functions are defined.

# data.py
from student import Student
import csv
from typing import List,Dict 


import csv
from typing import List
from student import Student

def export_to_csv(students: List[Student], subjects: List[str], filename: str = "students.csv") -> None:
    """
    Export students to a CSV file.

    Columns:
    name, section, <subjects...>, average
    """
    fieldnames = ["name", "section"] + subjects + ["average"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for student in students:
            writer.writerow(student.to_dict(subjects))

def import_from_csv(subjects: List[str], filename: str = "students.csv") -> List[Student]:
    """
    Import students from a CSV file and return a list of Student objects.
    """
    students: List[Student] = []

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = (row.get("name") or "").strip()
                section = (row.get("section") or "").strip().upper()

                grades: dict[str, float] = {}
                for subject in subjects:
                    raw = (row.get(subject) or "").strip()
                    if raw == "":
                        continue
                    try:
                        grades[subject] = float(raw)
                    except ValueError:
                        grades[subject] = 0.0

                # Build Student object (OOP)
                student = Student(name=name, section=section, scores=grades)
                students.append(student)

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")

    return students