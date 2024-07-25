import json
from constant import *

def BasicSettingMenu(*args):
    return [*args]

def settings_LBL_CB():
    SLC = {
    Preview_data : BasicSettingMenu(*Preview_data_parmeters),
    Startup_mode : BasicSettingMenu(*Startup_mode_parmeters),
    Font_Changed : BasicSettingMenu(*Font_Changed_parmeters)
    }
    
    return SLC

def SetData():
    SLC = settings_LBL_CB()
    
    setData_ = {
        "Settings_LBL_CB.json" : {    
            Preview_data : ("테이블 미리보기 여부", SLC[Preview_data]),
            Startup_mode : ("시작시 모드 여부", SLC[Startup_mode]),
            Font_Changed : ("폰트 변경 (재시작 필요)", SLC[Font_Changed])
            
        },

        "Settings_BTN.json": {
            "Save": ("설정을 저장합니다."),
            "developer": ("developer!"),
        }
    }

    return setData_

def SetDefault():
    SLC = settings_LBL_CB()
    
    SetDataDefault = {
        "Settings.json": {
            Preview_data : SLC[Preview_data][Preview_data_default],
            Startup_mode : SLC[Startup_mode][Startup_mode_default],
            Font_Changed : SLC[Font_Changed][Font_Changed_default],
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
        with open(SettingsWritePath % filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(filedata, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    SetSaved()
    SetSaved(SetDefault())
    print("Saved!")