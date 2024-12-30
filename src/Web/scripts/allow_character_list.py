import requests

# URL of the target server
url = "http://10.12.153.8:30099/"

# List of characters to test
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:',.<>?/`~"

# Function to test a single character
def test_character(char):
    data = {'ip': "127.0.0.1" + char}
    response = requests.post(url, data=data)
    if r"no" in response.text:
        return False
    return True

# Iterate through the characters and test each one
allowed_characters = []
for char in characters:
    if test_character(char):
        allowed_characters.append(char)
        print(char)

print("Allowed characters:", "".join(allowed_characters))