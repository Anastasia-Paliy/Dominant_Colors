import json

with open("color_names.json", 'r') as file:
        color_names = json.load(file)
print(color_names)
