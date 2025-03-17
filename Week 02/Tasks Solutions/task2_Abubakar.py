def check_last_letter_vowel(input_string):
    vowels = "aeiouAEIOU"
    if not input_string:
        return "Empty string provided"
    last_letter = input_string[-1]
    if last_letter.isalpha():
        if last_letter in vowels:
            return "vowel"
        else:
            return "consonant"
    else:
        return "Last character is not a letter"

if __name__ == "__main__":
    user_input = input("Enter a string: ")
    result = check_last_letter_vowel(user_input)
    print(f"The last letter is a {result}")