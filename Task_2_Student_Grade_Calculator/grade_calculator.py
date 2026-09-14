"""Student Grade Calculator for Week 2 of The Developers Arena internship."""


def calculate_grade(marks: int) -> tuple[str, str]:
    """Return the grade and an encouraging message for the given marks."""
    # The conditions are checked from the highest grade to the lowest grade.
    if marks >= 90:
        return "A", "Excellent work! Keep it up!"
    elif marks >= 80:
        return "B", "Very good! Keep working hard!"
    elif marks >= 70:
        return "C", "Good effort! You can improve even more!"
    elif marks >= 60:
        return "D", "Keep practicing! You can do better!"
    else:
        return "F", "Do not give up! Keep learning and try again!"


def main() -> None:
    """Collect student details, calculate a grade, and display the result."""
    print("=" * 40)
    print("       STUDENT GRADE CALCULATOR")
    print("=" * 40)
    print()

    student_name: str = input("Enter student name: ").strip()

    # Keep asking until the user enters a whole number from 0 to 100.
    while True:
        marks_input: str = input("Enter marks (0-100): ").strip()

        try:
            marks = int(marks_input)
        except ValueError:
            print("Invalid marks! Please enter a whole number between 0 and 100.")
            print()
            continue

        if 0 <= marks <= 100:
            break

        print("Invalid marks! Please enter a value between 0 and 100.")
        print()

    grade, message = calculate_grade(marks)

    print()
    print(f"Student: {student_name}")
    print(f"Marks: {marks}/100")
    print(f"Grade: {grade}")
    print(f"Message: {message}")


if __name__ == "__main__":
    main()
