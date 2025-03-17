def search_and_replace(file_path: str, search_word: str, replace_word: str) -> None:
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        modified_content = content.replace(search_word, replace_word)
        
        with open(file_path, 'w') as file:
            file.write(modified_content)
        
        print(f"Replaced '{search_word}' with '{replace_word}'")
        print("Original content:", content)
        print("Modified content:", modified_content)
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
search_and_replace('task2.txt', 'sample', 'task2')