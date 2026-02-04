import actions
import data
from menu import show_menu, get_menu_options


def main() -> None:
    students = []

    while True:
        show_menu()
        option = get_menu_options()

        if option == 1:
            actions.add_n_students(students)

        elif option == 2:
           actions.print_students(students)


        elif option == 3:
            if not students:
                print("No students available to calculate Top 3.")
                continue

            top3 = actions.get_top_3_students(students)

            print("\n=== Top 3 Students by Average Grade ===")
            for i, s in enumerate(top3, start=1):
                print(f"{i}. {s['name']} ({s['section']}) - Average: {s['average']:.2f}")

        elif option == 4:
            if not students:
                print("No students available to calculate overall class average.")
                continue

            avg = actions.overall_class_average(students)
            print(f"\n=== Overall Class Average ===\nAverage of all students: {avg:.2f}")

        elif option == 5:
            if not students:
                print("No students to export.")
            else:
                data.export_to_csv(students, actions.Subjects, "students.csv")
                print("Exported to students.csv successfully.")

        elif option == 6:
            try:
                students = data.import_from_csv(actions.Subjects, "students.csv")
                print(f"Imported {len(students)} students from students.csv successfully.")
            except FileNotFoundError:
                print("No previously exported CSV file was found (students.csv).")

        elif option == 7:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
