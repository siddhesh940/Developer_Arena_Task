# Week 1 Personal Introduction Program
# This program asks for user input and displays a personalized welcome message

# Get user's name
name: str = input("What is your name? ")

# Get user's age
age: str = input("How old are you? ")

# Get user's favorite hobby
hobby: str = input("What is your favorite hobby? ")

# Display a friendly personalized welcome message using f-string
print()
print("✨ Welcome " + name + "! ✨")
print(f"You are {age} years old and love {hobby}.")
