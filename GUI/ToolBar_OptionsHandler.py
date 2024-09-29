from PyQt5.QtWidgets import (
    QWidget,
    )

from GUIStyle import *
from Json_Utils import *
from Settings_JSON_Write import *
from config_paths import *
from applog import *

logger = InitLogger(CurrentFileName(__file__))


# 설정 불러오기/저장하기를 구성하는 클래스
class OptionsHandler(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        # 부모 객체 매개변수 정의
        self.parent = parent
        self.CBDict = self.parent.CBDict
        
    def CBSetValueRead(self):
        try:
            self.ApplySettingValue()

        # 파일이 없을때 예외처리, 파일은 존재하지만 내용이 없을때 예외처리
        except (FileNotFoundError, json.JSONDecodeError) as e:
            SetSaved(SetDefault())
            self.ApplySettingValue()
        
        except Exception as e:  
            logger.error(f"설정 불러오기를 적용하는 과정에 문제가 생겼습니다. | Error Code: {e}")
    
    def ApplySettingValue(self):
        SetData = OpenJson(SetDataFilePath)
        for label, comboboxObj in self.CBDict.items():
            setLabel = SetData.get(label)
            if setLabel is not None:
                comboboxObj.setCurrentText(setLabel)
                logger.info(f"설정 불러오기 성공: {label} - {setLabel}")
            else:
                logger.error(f"설정 불러오기 실패: {label} - {setLabel}")

    # 콤보박스의 선택된 값을 *.json 으로 저장함.
    # 이것은 메인 GUI에 기능을 비활성화거나 화성화할때 사용되는 값.
    def CBValueSave(self):
        CBSetValueTemp = {} # 임시 설정 저장

        for Lable, combobox in self.CBDict.items():
            CBSetValueTemp[Lable] = combobox.currentText()
            # 설정 불러오기 배열값 저장
            try:
                SaveJSON(SetDataFilePath, CBSetValueTemp)
                logger.info(f"{Lable} - {combobox.currentText()} 설정 값이 저장됨.")
            
            except Exception as e:
                logger.error(f"설정값을 저장하는 데에 문제가 생겼습니다. | Error Code: {e}")
                logger.error(f"{Lable} - {combobox.currentText()} 설정 값 저장을 실패함.")