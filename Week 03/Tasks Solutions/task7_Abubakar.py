def replace_letter_in_file(file_path: str, old_letter: str, new_letter: str) -> None:
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        modified_content = content.replace(old_letter, new_letter)
        
        with open(file_path, 'w') as file:
            file.write(modified_content)
        
        print(f"Letter replacement complete. Replaced '{old_letter}' with '{new_letter}'.")
        print(f"Modified content:\n{modified_content}")
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
replace_letter_in_file('task7_replacement_needed.txt', 'I', 'He')