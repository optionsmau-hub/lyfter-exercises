#data.py
# This file can be used to store any data-related functions or constants
# For now, it is left empty as no specific data functions are defined.

# data.py

import csv
from typing import List, Dict


def export_to_csv(students: List[Dict], subjects: List[str], filename: str = "students.csv") -> None:
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
            row = {
                "name": student["name"],
                "section": student["section"],
                "average": f"{student['average']:.2f}",
            }

            # Copy grades into row using subject names as columns
            for subject in subjects:
                row[subject] = student["grades"].get(subject, "")

            writer.writerow(row)


def import_from_csv(subjects: List[str], filename: str = "students.csv") -> List[Dict]:
    """
    Import students from a CSV file.
    Rebuilds the structure:
    {
      'name': ...,
      'section': ...,
      'grades': {...},
      'average': float
    }
    """
    students: List[Dict] = []

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = (row.get("name") or "").strip()
                section = (row.get("section") or "").strip().upper()

                grades: Dict[str, int] = {}
                for subject in subjects:
                    raw = (row.get(subject) or "").strip()
                    # Convert to int safely; if empty or invalid, set 0 (or you can skip)
                    try:
                        grades[subject] = int(float(raw))
                    except ValueError:
                        grades[subject] = 0

                # Prefer recalculating average (more reliable)
                average = sum(grades.values()) / len(subjects) if subjects else 0.0

                students.append(
                    {
                        "name": name,
                        "section": section,
                        "grades": grades,
                        "average": average,
                    }
                )

    except FileNotFoundError:
        # Let the caller decide what to print; raise for clarity
        raise FileNotFoundError(f"File not found: {filename}")

    return students
