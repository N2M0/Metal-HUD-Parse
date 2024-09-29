import json
from config_paths import *
from applog import *

logger = InitLogger(CurrentFileName(__file__))


def create_settings_data(is_default=False):
    return {
        Preview_data: ("테이블 미리보기 여부", Preview_data_parmeters) if not is_default else (Preview_data_parmeters[Preview_data_default]),
        Preview_data_viewing_mode: ("테이블 미리보기 보기 모드", Preview_data_viewing_mode_parmeters) if not is_default else (Preview_data_viewing_mode_parmeters[Preview_data_viewing_mode_default]),
        Startup_mode: ("시작시 모드 여부", Startup_mode_parmeters) if not is_default else (Startup_mode_parmeters[Startup_mode_default]),
        Font_Changed: ("폰트 변경 (재시작 필요)", Font_Changed_parmeters) if not is_default else (Font_Changed_parmeters[Font_Changed_default]),
        Include_Index_In_File_Parse_data: ("Parse 파일 데이터에 인덱스 포함 여부", Include_Index_In_File_Parse_data_parameters) if not is_default else (Include_Index_In_File_Parse_data_parameters[Include_Index_In_File_Parse_data_default]),
        }

# 레이블 - 콤보박스 - 버튼 데이터
def SetData():
    return {
        "Settings_LBL_CB.json": create_settings_data(False),
        "Settings_BTN.json": {
            "Save": ("설정을 저장합니다."),
            "developer": ("developer!"),
        }
    }

# 설정 데이터 기본값
def SetDefault():
    return {
        "Settings.json": create_settings_data(True)
    }

# 설정 데이터 저장
def SetSaved(setData_=None):
    data = setData_ if setData_ is not None else None
    
    if data is not None:
        for filename, filedata in data.items():
            with open(SettingsWritePath % filename, "w", encoding="utf-8") as f:
                json.dump(filedata, f, ensure_ascii=False, indent=4)
            logger.info(f"'{filename}': 설정 데이터가 생성되었습니다.")
        
    else:
        logger.error(f"'{filename}': 설정 데이터가 {data} 입니다.")

if __name__ == "__main__":
    SetSaved(SetData())
    SetSaved(SetDefault())