import json

def OpenJson(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)