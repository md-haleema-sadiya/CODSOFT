#simple calculator

# This function takes two numbers as input and returns their sum.
def add(num1, num2):
    return num1 + num2

# This function takes two numbers as input and returns their difference.
def subtract(num1, num2):
    return num1 - num2

# This function takes two numbers as input and returns their product.
def multiply(num1, num2):
    return num1 * num2

# This function takes two numbers as input and returns their quotient.
def divide(num1, num2):
    # Check if the second number is zero to avoid division by zero error
    if num2 == 0:
        return "Error: Division by zero is not allowed."
    return num1 / num2

# Display a welcome message to the user
print("------Welcome to my Calculator!------")

#show the user the available operations
print("\nChoose an operation:")
print("  1. Addition       (+)")
print("  2. Subtraction    (-)")
print("  3. Multiplication (*)")
print("  4. Division       (/)")

#ask the user to choose an operation
choice = input("\nEnter your choice (1/2/3/4): ")

#ask the user to enter two numbers
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: ")) # Convert the input to float for decimal calculations

# Perform the chosen operation and display the result
if choice == '1':
    result = add(num1, num2)
    print(f"\n{num1} + {num2} = {result}")
 
elif choice == '2':
    result = subtract(num1, num2)
    print(f"\n{num1} - {num2} = {result}")
 
elif choice == '3':
    result = multiply(num1, num2)
    print(f"\n{num1} * {num2} = {result}")
 
elif choice == '4':
    result = divide(num1, num2)
    print(f"\n{num1} / {num2} = {result}")
 
else:
    # If the user enters something other than 1, 2, 3, or 4
    print("\nInvalid choice! Please enter 1, 2, 3, or 4.")

# Display a goodbye message to the user
print("\n------Thank you for using my Calculator :) Goodbye!------")