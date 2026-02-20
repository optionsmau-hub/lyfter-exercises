from typing import List
from student import Student

Subjects = ["English", "Spanish", "Science", "Social Studies"]


def is_valid_name(name: str) -> bool:
    """Valid name: non-empty, letters and spaces only."""
    name = name.strip()
    return bool(name) and name.replace(" ", "").isalpha()


def is_valid_section(section: str) -> bool:
    """Valid section: 1-2 digits followed by 1 letter, e.g. 10A, 11B, 9C."""
    section = section.strip().upper()

    if len(section) < 2 or len(section) > 3:
        return False

    number_part = section[:-1]
    letter_part = section[-1]

    return number_part.isdigit() and letter_part.isalpha()


def student_exists(students: List[Student], name: str, section: str) -> bool:
    """Check if a student with same name and section already exists."""
    name = name.strip().lower()
    section = section.strip().upper()

    for student in students:
        if student.name.strip().lower() == name and student.section.strip().upper() == section:
            return True
    return False


def input_grade(subject: str) -> int:
    """Ask for a grade (0-100) and keep asking until valid."""
    while True:
        value = input(f"Enter {subject} grade (0-100): ").strip()
        if value.isdigit():
            grade = int(value)
            if 0 <= grade <= 100:
                return grade
        print("Invalid grade. Please enter a number between 0 and 100.")


from student import Student

def create_student(students: List[Student]) -> Student | None:
    """Create one Student object. Returns None if duplicate."""

    while True:
        name = input("Full name: ").strip()
        if is_valid_name(name):
            break
        print("Invalid name. Use letters and spaces only.")

    while True:
        section = input("Section (e.g. 11B): ").strip().upper()
        if is_valid_section(section):
            break
        print("Invalid section format. Example: 10A, 11B.")

    if student_exists(students, name, section):
        print("Student already exists (same name and section).")
        return None

    scores = {}
    for subject in Subjects:
        scores[subject] = input_grade(subject)

    # Create Student object instead of dict
    student = Student(name=name, section=section, scores=scores)

    return student


def add_n_students(students: List[Student]) -> None:
    """Ask how many students to add and append them to the list."""
    while True:
        n = input("How many students do you want to enter? ").strip()
        if n.isdigit() and int(n) > 0:
            n = int(n)
            break
        print("Invalid number. Please enter a whole number greater than 0.")

    added = 0
    while added < n:
        print(f"\n--- Student {added + 1} of {n} ---")
        student = create_student(students)
        if student is None:
            print("Try again.")
            continue
        students.append(student)
        added += 1


def print_students(students: List[Student]) -> None:
    """Print all students and their grades."""
    if not students:
        print("No students to display.")
        return

    print("\n== Students ==")
    for i, s in enumerate(students, start=1):
        print(f"{i}. {s.name} ({s.section}) - Average: {s.average:.2f}")

        for subject, grade in s.scores.items():
            print(f"   - {subject}: {grade}")
        print()


def get_top_3_students(students: List[Student]) -> List[Student]:
    """Return the top 3 students by average grade (descending)."""
    if not students:
        return []

    return sorted(students, key=lambda s: s.average, reverse=True)[:3]

def overall_class_average(students: List[Student]) -> float:
    """Return the average of all students' averages."""
    if not students:
        return 0.0

    total = sum(s.average for s in students)
    return total / len(students)
