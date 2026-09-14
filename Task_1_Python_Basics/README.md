# Week 1: Personal Introduction Program

## Project Overview

This is a Week 1 Python Basics internship project for The Developers Arena. The program demonstrates fundamental Python concepts for beginners, including:

- **Variables**: Storing user data in memory
- **input()**: Getting information from the user
- **print()**: Displaying output to the user
- **Strings**: Working with text data
- **f-strings**: Formatting personalized messages
- **Basic program execution**: Running a complete Python script

This is a beginner-friendly project designed to practice basic Python programming concepts and user interaction.

## Objective

Create a simple Python program that collects personal information from the user (name, age, hobby) and displays a personalized welcome message.

## Technologies Used

- **Language**: Python 3.x
- **Concepts**: Variables, input/output, string formatting
- **No external dependencies** - uses only Python built-in functions

## Features

✨ **Simple and Interactive**: Easy-to-understand user prompts

✨ **Personalized Output**: Uses f-strings to create a customized welcome message

✨ **Beginner-Friendly**: Well-commented code that explains each step

✨ **Clean Code**: Readable and maintainable for learning purposes

## Project Structure

```
Week1_Task/
├── README.md
├── personal_intro.py
└── requirements.txt
```

## Setup / Installation Instructions

### Prerequisites

- **Python 3.x** (Python 3.6 or higher recommended)
- **VS Code** (or any text editor)
- **Windows OS** (or macOS/Linux)

### Verify Python Installation

Open Command Prompt or Terminal and run:

```
python --version
```

You should see output like: `Python 3.x.x`

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

### Setup Steps

1. Navigate to the project folder:

   ```
   cd D:\Developer_Arena\Week1_Task
   ```

2. Verify all files are present:
   - personal_intro.py
   - README.md
   - requirements.txt

3. No external packages need to be installed (all built-in Python functions)

## How to Run the Program

1. Open Command Prompt and navigate to the project folder:

   ```
   cd D:\Developer_Arena\Week1_Task
   ```

2. Run the program:

   ```
   python personal_intro.py
   ```

3. Follow the on-screen prompts and enter your information

4. View your personalized welcome message

## Example Input and Output

### Sample Run:

```
What is your name? Alex
How old are you? 21
What is your favorite hobby? Coding

✨ Welcome Alex! ✨
You are 21 years old and love Coding.
```

### Another Example:

```
What is your name? Jordan
How old are you? 19
What is your favorite hobby? Gaming

✨ Welcome Jordan! ✨
You are 19 years old and love Gaming.
```

## Code Explanation

### Step 1: Get the Name

```python
name = input("What is your name? ")
```

- Uses `input()` function to prompt the user for their name
- Stores the response in the `name` variable

### Step 2: Get the Age

```python
age = input("How old are you? ")
```

- Prompts the user for their age
- Stores the response in the `age` variable

### Step 3: Get the Hobby

```python
hobby = input("What is your favorite hobby? ")
```

- Prompts the user for their favorite hobby
- Stores the response in the `hobby` variable

### Step 4: Display the Welcome Message

```python
print()
print("✨ Welcome " + name + "! ✨")
print(f"You are {age} years old and love {hobby}.")
```

- Prints a blank line for readability
- Displays a personalized welcome message using string concatenation
- Uses an **f-string** to insert variables into the final message
- F-strings allow easy variable insertion using curly braces `{}`

## Technical Requirements Fulfilled

✅ **Uses input()**: Program uses `input()` function 3 times to get user information (name, age, hobby)

✅ **Stores in variables**: Each response is stored in variables:

- `name` variable stores the user's name
- `age` variable stores the user's age
- `hobby` variable stores the user's favorite hobby

✅ **Uses print()**: Program uses `print()` to display the welcome message

✅ **At least 3 variables**: The program uses exactly 3 variables: `name`, `age`, and `hobby`

✅ **Uses f-string**: Final message uses f-string formatting: `f"You are {age} years old and love {hobby}."`

✅ **Personalized welcome message**: Message is customized with user's actual input

✅ **Beginner-friendly with comments**: Code includes comments explaining important parts

✅ **Clean and readable**: Code is well-formatted and easy to understand

## Testing

The program was tested with the following sample inputs:

**Test Case 1:**

- Input: Name = "Alex", Age = "21", Hobby = "Coding"
- Expected Output: A personalized message welcoming Alex, mentioning their age and hobby
- Result: ✅ **PASS** - Program correctly displays the personalized welcome message

**Test Case 2:**

- Input: Name = "Jordan", Age = "19", Hobby = "Gaming"
- Expected Output: A personalized message welcoming Jordan
- Result: ✅ **PASS** - Program works correctly with different inputs

**Test Case 3:**

- Input: Empty or whitespace values
- Result: ✅ **PASS** - Program accepts input and displays it, allowing user flexibility

The program runs without errors and produces the expected output.

## What I Learned

### Python Basics Covered

1. **Variables**: Learned how to create and use variables to store data
   - Variables hold information for later use
   - Variable names should be descriptive

2. **input() Function**: Learned how to get user input
   - `input()` pauses the program and waits for user input
   - User input is always received as a string

3. **print() Function**: Learned how to display output
   - `print()` displays text to the user
   - Multiple `print()` calls create separate lines

4. **Strings and String Concatenation**: Learned how to work with text
   - Strings are sequences of characters enclosed in quotes
   - Strings can be combined using the `+` operator

5. **f-strings**: Learned modern string formatting
   - F-strings allow variables to be inserted directly into strings
   - Syntax: `f"Text {variable} more text"`
   - F-strings are more readable than older formatting methods

6. **Program Flow**: Learned how a Python program executes sequentially
   - Each line of code runs in order
   - The program waits for user input at each prompt

### Key Takeaways

- Writing simple, clean code is better than complex code
- Comments help explain code to others and to yourself later
- User interaction makes programs more engaging
- Python's simplicity makes it great for beginners
- Variable names should be meaningful and descriptive

---

**Project Status**: ✅ Complete and Ready for Submission

**Author**: Week 1 Intern - The Developers Arena

**Date**: 2026

**Version**: 1.0
