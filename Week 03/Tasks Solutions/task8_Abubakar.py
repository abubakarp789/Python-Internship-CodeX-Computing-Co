def divide_numbers() -> None:
    try:
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        result = num1 / num2
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
    except ValueError:
        print("Error: Invalid input. Please enter numbers only.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
divide_numbers()