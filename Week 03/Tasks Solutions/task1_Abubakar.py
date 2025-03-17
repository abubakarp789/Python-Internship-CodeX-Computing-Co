def count_characters_and_words(file_path: str) -> None:
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            num_characters = len(content)
            num_words = len(content.split())
            print(f"Number of characters: {num_characters}")
            print(f"Number of words: {num_words}")
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
count_characters_and_words('task1.txt')