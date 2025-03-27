import re

# Open the text document
with open('Week 04/document.txt', 'r') as file:
    text = file.read()

# Regular expression pattern to match dates in the format MM/DD/YYYY
pattern1 = r'\d{2}/\d{2}/\d{4}'

# Regular expression pattern to match dates in the format YYYY-MM-DD
pattern2 = r'\d{4}-\d{2}-\d{2}'

# Regular expression pattern to match dates in the format MMM DD, YYYY
pattern3 = r'[A-Za-z]{5} \d{2}, \d{4}'

# Find all dates in the text using the regular expression patterns
dates1 = re.findall(pattern1, text)
dates2 = re.findall(pattern2, text)
dates3 = re.findall(pattern3, text)

# Print the extracted dates
print("Dates in the format MM/DD/YYYY:")
print(dates1)

print("Dates in the format YYYY-MM-DD:")
print(dates2)

print("Dates in the format MM DD, YYYY:")
print(dates3)