import json

# json 열기
def OpenJson(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
    
# json 저장
def SaveJSON(filename, data):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)