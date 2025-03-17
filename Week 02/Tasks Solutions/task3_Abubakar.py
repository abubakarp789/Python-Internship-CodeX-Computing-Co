def employee_salary(employee_name, monthly_salary=10000):
    tax_percentage = 2
    tax_amount = (tax_percentage / 100) * monthly_salary
    salary_after_tax = monthly_salary - tax_amount
    print(f"Employee Name: {employee_name}")
    print(f"Salary after {tax_percentage}% tax deduction: {salary_after_tax}")

if __name__ == "__main__":
    name = input("Enter employee name: ")
    salary_input = input("Enter monthly salary (press Enter for default 10000): ")
    if salary_input:
        salary = float(salary_input)
        employee_salary(name, salary)
    else:
        employee_salary(name)