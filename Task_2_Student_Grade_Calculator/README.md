# Student Grade Calculator

## 1. Project Overview

This is the Week 2 internship project for The Developers Arena. It demonstrates decision-making, loops, functions, input validation, and grading logic in Python.

## 2. Objectives

The objectives of this project are to:

- Understand `if-elif-else` statements.
- Use comparison operators.
- Use `while` loops.
- Create functions.
- Validate user input.
- Display meaningful output.

## 3. Technologies Used

- Python 3.x
- Visual Studio Code
- Git
- GitHub

No external Python libraries are required.

## 4. Features

- Student name input
- Marks input
- Marks validation
- Grade calculation
- Encouraging messages
- Invalid input handling
- Loop-based validation

## 5. Grading Logic

| Grade | Marks  |
| ----- | ------ |
| A     | 90-100 |
| B     | 80-89  |
| C     | 70-79  |
| D     | 60-69  |
| F     | 0-59   |

## 6. Project Structure

```text
Task_2_Student_Grade_Calculator/
├── grade_calculator.py
├── README.md
├── test_cases.txt
└── screenshots/
```

The `screenshots/` folder is reserved for screenshots added manually after testing.

## 7. Setup Instructions

Verify that Python is installed:

```text
python --version
```

Open the repository folder in Visual Studio Code. The project is located at `Task_2_Student_Grade_Calculator`.

## 8. How to Run

From the repository root, run:

```text
cd Task_2_Student_Grade_Calculator
python grade_calculator.py
```

## 9. Code Structure

- `calculate_grade()` uses `if-elif-else` grading logic and returns an encouraging message.
- `main()` collects the student's name and marks.
- A `while` loop validates the marks and repeats for invalid input.
- The output section displays the student name, marks, grade, and message.

## 10. Technical Requirements Fulfilled

| Requirement            | How it is satisfied                                     |
| ---------------------- | ------------------------------------------------------- |
| `if-elif-else` grading | `calculate_grade()` selects A, B, C, D, or F.           |
| Marks validation       | Marks must be a whole number from 0 to 100.             |
| At least one function  | The program defines `calculate_grade()` and `main()`.   |
| Encouraging messages   | Every grade returns a positive message.                 |
| `while` loop           | Invalid marks cause the program to ask again.           |
| User input             | `input()` collects the student name and marks.          |
| Correct grade ranges   | The program follows the A, B, C, D, and F ranges above. |

## 11. Testing

The following cases should be tested:

1. A grade: enter `95` and expect grade A.
2. B grade: enter `85` and expect grade B.
3. C grade: enter `75` and expect grade C.
4. D grade: enter `65` and expect grade D.
5. F grade: enter `50` and expect grade F.
6. Invalid marks below 0: enter `-10`; the program should reject it and ask again.
7. Invalid marks above 100: enter `110`; the program should reject it and ask again.
8. Non-numeric input: enter `abc`; the program should reject it and ask again.

Verified on 2026-09-14: all five grade cases produced the expected grade. The program also rejected `-10`, `110`, and `abc`, then accepted `85` and produced grade B. Screenshots will demonstrate successful A/B/C/D/F grade calculation, invalid input validation, and successful program execution after they are added manually.

## 12. What I Learned

This project practices conditional statements, comparison operators, loops, functions, input validation, and error handling with `try` and `except`.

## 13. Conclusion

The Student Grade Calculator is a simple Python program that validates marks, calculates the correct grade, and gives the student an encouraging message.
