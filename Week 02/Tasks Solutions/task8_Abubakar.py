def Capital_Convertor():
    name = input("Enter your name: ")
    return name.upper()

if __name__ == "__main__":
    capital_name = Capital_Convertor()
    print(f"Name in capital letters: {capital_name}")