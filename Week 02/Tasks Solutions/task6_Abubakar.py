def calculate_average_temperature(temperatures):
    if not temperatures:
        return 0  # Return 0 if the list is empty to avoid division by zero
    return sum(temperatures) / len(temperatures)

def find_highest_temperature(temperatures):
    if not temperatures:
        return None # Return None for an empty list
    return max(temperatures)

def find_lowest_temperature(temperatures):
    if not temperatures:
        return None # Return None for an empty list
    return min(temperatures)

def sort_temperatures_ascending(temperatures):
    return sorted(temperatures)

def remove_temperature_by_index(temperatures, index_to_remove):
    if 0 <= index_to_remove < len(temperatures):
        removed_temperature = temperatures.pop(index_to_remove)
        return removed_temperature, temperatures
    else:
        return None, temperatures # Return None for removed temperature if index is invalid


if __name__ == "__main__":
    temperatures_celsius = [22, 24, 30, 35, 29, 22, 20, 19]

    # Calculate and print the average temperature
    average_temp = calculate_average_temperature(temperatures_celsius)
    print(f"Average temperature for the month: {average_temp:.2f}°C")

    # Find and print the highest and lowest temperatures
    highest_temp = find_highest_temperature(temperatures_celsius)
    lowest_temp = find_lowest_temperature(temperatures_celsius)
    print(f"Highest temperature: {highest_temp}°C")
    print(f"Lowest temperature: {lowest_temp}°C")

    # Sort the temperatures in ascending order
    sorted_temperatures = sort_temperatures_ascending(temperatures_celsius)
    print(f"Temperatures in ascending order: {sorted_temperatures}°C")

    # Remove the temperature record for a specific day (e.g., remove the first day's record)
    day_to_remove_index = 0 # Removing the first day
    removed_temperature, updated_temperatures = remove_temperature_by_index(temperatures_celsius, day_to_remove_index)
    if removed_temperature is not None:
        print(f"Removed temperature for day {day_to_remove_index + 1}: {removed_temperature}°C")
        print(f"Temperatures after removing day {day_to_remove_index + 1}: {updated_temperatures}°C")
    else:
        print("Invalid day index to remove.")