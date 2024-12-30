# Define the strings and the hex values
string1 = "welcome_to_2024hustncc!!!!"
hex_values = "01 08 0F 18 1B 05 0C 2C 2B 06 2C 6D 51 6D 47 01 18 03 18 0B 3C 11 44 57 0F 5C"

# Convert hex values to a list of integers
hex_list = [int(x, 16) for x in hex_values.split()]

# XOR each character in string1 with the corresponding hex value
result = ''.join([chr(ord(c) ^ h) for c, h in zip(string1, hex_list)])

# Output the result
result
