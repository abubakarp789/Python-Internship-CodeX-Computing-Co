def list_to_dictionary(keys_list, values_list):
    if len(keys_list) != len(values_list):
        return "Error: Lists must have the same number of elements."

    result_dict = {}
    for i in range(len(keys_list)):
        result_dict[keys_list[i]] = values_list[i]
    return result_dict

if __name__ == "__main__":
    keys = []
    values = []
    n = int(input("Enter the number of elements for the lists: "))
    print("Enter elements for the first list (keys):")
    for _ in range(n):
        keys.append(input())
    print("Enter elements for the second list (values):")
    for _ in range(n):
        values.append(input())

    dictionary = list_to_dictionary(keys, values)
    if isinstance(dictionary, str): # Check if an error message string was returned
        print(dictionary)
    else:
        print("Dictionary created from the lists:")
        print(dictionary)