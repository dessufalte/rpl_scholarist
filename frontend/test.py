import os
import json

file_name = 'frontend/test.json'
file_path = os.path.join(os.getcwd(), file_name)

print(f"Looking for: {file_path}")  # Debug path
with open(file_path, 'r') as file:
    data = json.load(file)

print(data)
