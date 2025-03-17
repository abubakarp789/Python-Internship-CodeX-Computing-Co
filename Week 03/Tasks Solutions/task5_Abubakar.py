import json

def save_and_find_max_age(dictionary: dict, file_path: str) -> None:
    try:
        with open(file_path, 'w') as file:
            json.dump(dictionary, file)
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        max_age = max(data.values())
        max_age_names = [name for name, age in data.items() if age == max_age]
        
        print(f"Person(s) with the maximum age ({max_age}): {', '.join(max_age_names)}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
dictionary = {'Ali': 23, 'Saad': 24, 'Salman': 15, 'Shams': 25, 'Sadiq': 46, 'Hammad': 23}
save_and_find_max_age(dictionary, 'task5_ages.json')