def multiply_list_numbers(numbers_list):
    if not numbers_list:
        return 1  # Return 1 for an empty list as the multiplicative identity
    product = 1
    for number in numbers_list:
        product *= number
    return product

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    result = multiply_list_numbers(numbers)
    print(f"Multiplication of all numbers in the list: {result}")