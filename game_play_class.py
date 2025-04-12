import json

with open("drawing_hints.json") as json_file:
    json_data = json.load(json_file)
    print(json_data)
