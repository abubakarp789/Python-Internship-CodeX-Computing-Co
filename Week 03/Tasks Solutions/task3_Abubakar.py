def lists_to_dict(list1: list, list2: list, file_path: str) -> None:
    try:
        if len(list1) != len(list2):
            raise ValueError("Lists must have the same number of elements.")
        
        dictionary = {list1[i]: list2[i] for i in range(len(list1))}
        
        with open(file_path, 'w') as file:
            file.write(str(dictionary))
        
        print("Dictionary saved to file.")
        
        # Print the data saved in the file
        print(f"Data saved in file: {dictionary}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
lists_to_dict(['a', 'b', 'c'], [1, 2, 3], 'task3_dictionary.txt')