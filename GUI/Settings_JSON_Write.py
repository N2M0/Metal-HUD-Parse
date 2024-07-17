import json

def BasicSettingMenu():
    return ["used", "not used"]

def SetData():
    setData_ = {
        "Settings_LBL_CB.json" : {    
            "Preview data": ("테이블 미리보기 여부", BasicSettingMenu()),
            "Startup mode": ("시작시 모드 여부", BasicSettingMenu()),
            "test1": ("test1", BasicSettingMenu()),
            "test2": ("test2", BasicSettingMenu()),
            "test3": ("test3", BasicSettingMenu()),
            
        },

        "Settings_BTN.json": {
            "Save": ("설정을 저장합니다."),
            "Next": ("Next합니다."),
            "END": ("END합니다."),
            "Home": ("Home합니다.")
        }
    }

    return setData_

def SetSaved(setData_=False):
    # tuple 로 유지할것
    for filename, filedata in SetData().items():
        with open(rf"GUI\Settings\{filename}", "w", encoding="utf-8") as f:
            f.write(json.dumps(filedata, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    SetSaved()
    print("Saved!")