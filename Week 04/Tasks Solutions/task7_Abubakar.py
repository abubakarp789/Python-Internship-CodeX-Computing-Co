import re

def extract_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails

# Example usage
text = "Hello, my email is john.doe@example.com. Please contact me at jane.smith@example.com."
emails = extract_emails(text)
print(emails)