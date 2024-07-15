import json

setData = {
    "Settings_LBL_CB.json" : {    
        "Preview data": ("테이블 미리보기 여부", ["Test1", "test2"]),
        "Startup mode": ("시작시 모드 여부", ["Test1", "Test3", "Test4"]),
        "test1": ("test1", ["Test1", "Test3", "Test4"]),
        "test2": ("test2", ["Test1", "Test3", "Test4"]),
        "test3": ("test3", ["Test1", "Test3", "Test4"]),
        
    },

    "Settings_BTN.json": {
        "Save": ("설정을 저장합니다."),
        "Next": ("Next합니다."),
        "END": ("END합니다."),
        "Home": ("Home합니다.")
    }
}

# tuple 로 유지할것
for filename, filedata in setData.items():
    with open(rf"Metal-HUD-Parse\GUI\Settings\{filename}", "w", encoding="utf-8") as f:
        f.write(json.dumps(filedata, ensure_ascii=False, indent=4))