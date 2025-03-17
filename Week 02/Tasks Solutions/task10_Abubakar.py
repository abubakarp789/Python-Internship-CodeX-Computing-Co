def calculate_discounted_bill(total_purchase_amount):
    discount_percentage = 0
    if total_purchase_amount > 1000:
        discount_percentage = 20
    elif total_purchase_amount > 500:
        discount_percentage = 10

    discount_amount = (discount_percentage / 100) * total_purchase_amount
    final_bill = total_purchase_amount - discount_amount
    return final_bill, discount_percentage

if __name__ == "__main__":
    purchase_amount = float(input("Enter total purchase amount: $"))
    final_bill, discount = calculate_discounted_bill(purchase_amount)
    print(f"Total Purchase Amount: ${purchase_amount:.2f}")
    print(f"Discount Applied: {discount}%")
    print(f"Final Bill after discount: ${final_bill:.2f}")

# Explanation for function efficiency:
# Using a function like calculate_discounted_bill makes the code more efficient because:
# 1. Reusability: The discount logic is encapsulated within the function. If we need to calculate discounts at multiple points in our program (e.g., for different customers or items), we can simply call this function again and again without rewriting the discount calculation logic.
# 2. Modularity: The function breaks down the larger task of bill calculation into a smaller, manageable, and logical unit (discount calculation). This makes the code easier to understand, debug, and maintain.
# 3. Readability:  The function gives a clear name to the discount calculation process, making the main part of the code more readable. Instead of seeing complex discount calculation logic inline, we see a function call `calculate_discounted_bill`, which clearly conveys the purpose.
# 4. Testability: Functions are easier to test in isolation. We can write unit tests specifically for the `calculate_discounted_bill` function to ensure it correctly applies discounts for different purchase amounts, without having to test the entire shopping platform code.