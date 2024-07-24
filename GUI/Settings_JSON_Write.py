import json
from constant import *

def BasicSettingMenu(*args):
    return [*args]

def settings_LBL_CB():
    SLC = {
    Preview_data : BasicSettingMenu(*Preview_data_parmeters),
    Startup_mode : BasicSettingMenu(*Startup_mode_parmeters)
    }
    
    return SLC

def SetData():
    SLC = settings_LBL_CB()
    Future_name = list(SLC.keys())
    
    setData_ = {
        "Settings_LBL_CB.json" : {    
            Future_name[0]: ("테이블 미리보기 여부", SLC["Preview data"]),
            Future_name[1]: ("시작시 모드 여부", SLC["Startup mode"])
            
        },

        "Settings_BTN.json": {
            "Save": ("설정을 저장합니다."),
            "developer": ("developer!"),
        }
    }

    return setData_

def SetDefault():
    SLC = settings_LBL_CB()
    Future_name = list(SLC.keys())
    
    SetDataDefault = {
        "Settings.json": {
            Future_name[0] : SLC["Preview data"][Preview_data_default],
            Future_name[1] : SLC["Startup mode"][Startup_mode_default],
            }
    }
    
    return SetDataDefault

def SetSaved(setData_ = None):
    
    if setData_ is not None:
        data = setData_
    else:
        data = SetData()
    
    # tuple 로 유지할것
    for filename, filedata in data.items():
        with open(rf"GUI\Settings\{filename}", "w", encoding="utf-8") as f:
            f.write(json.dumps(filedata, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    SetSaved()
    SetSaved(SetDefault())
    print("Saved!")