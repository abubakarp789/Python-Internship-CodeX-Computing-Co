def write_questions_to_file(file_path: str) -> None:
    try:
        sentence = input("Enter a sentence: ")
        if sentence.endswith('?'):
            with open(file_path, 'a') as file:
                file.write(sentence + '\n')
            print("Question saved to file.")
        else:
            print("The sentence is not a question.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
write_questions_to_file('task6_questions.txt')