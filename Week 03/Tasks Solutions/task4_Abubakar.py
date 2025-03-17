def save_employee_biodata(file_path: str) -> None:
    try:
        name = input("Enter name: ")
        cnic = input("Enter CNIC number: ")
        age = input("Enter age: ")
        salary = input("Enter salary: ")
        
        with open(file_path, 'w') as file:
            file.write(f"Name: {name}\nCNIC: {cnic}\nAge: {age}\nSalary: {salary}\n")
        
        contact_number = input("Enter contact number: ")
        
        with open(file_path, 'a') as file:
            file.write(f"Contact Number: {contact_number}\n")
        
        with open(file_path, 'r') as file:
            print(file.read())
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
save_employee_biodata('task4_employee_biodata.txt')