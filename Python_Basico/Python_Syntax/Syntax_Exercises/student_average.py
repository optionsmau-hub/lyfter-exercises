# Program to calculate statistics of a student's grades

def calculate_statistics(grades):
    if not grades:
        return None, None, None

    average = sum(grades) / len(grades)
    max_grade = max(grades)
    min_grade = min(grades)

    return average, max_grade, min_grade


# Example of use
student_grades = [85, 90, 78, 92, 88]

average, highest_grade, lowest_grade = calculate_statistics(student_grades)

print(f"Average: {average}")
print(f"Highest Grade: {highest_grade}")
print(f"Lowest Grade: {lowest_grade}")


# Function to determine if grade is passing
def is_passing(grade, passing_score=60):
    return grade >= passing_score


grade = 75

if is_passing(grade):
    print(f"The grade {grade} is passing.")
else:
    print(f"The grade {grade} is not passing.")
