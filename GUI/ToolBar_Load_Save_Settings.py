from PyQt5.QtWidgets import (
    QWidget,
    )

# from PyQt5.QtCore import Qt, QSize
from GUIStyle import *
from OpenJson import *
from SaveJSON import *
from Settings_JSON_Write import *

# 설정 불러오기/저장하기를 구성하는 클래스
class Load_Save_Settings(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # 부모 객체 매개변수 정의
        self.parent = parent
        self.CBDict = self.parent.CBDict
        self.AvoidDuplicateCreation = self.parent.AvoidDuplicateCreation
        
    def CBSetValueRead(self):
        try:
            SetData = OpenJson(r"GUI\Settings\Settings.json")
            for (Lable, comboboxObj), (setLable, SetComboboxIndex) in zip(self.CBDict.items(), SetData.items()):
                if Lable == setLable:
                    comboboxObj.setCurrentIndex(SetComboboxIndex)
                    print(f"설정 불러오기 성공: {Lable} - {setLable} - {SetComboboxIndex}")
                
                else:
                    print(f"설정 불러오기 실패: {Lable} - {setLable} - {SetComboboxIndex}")

        # 파일이 없을때 예외처리, 파일은 존재하지만 내용이 없을때 예외처리
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    

    # 콤보박스의 선택된 값을 *.json 으로 저장함.
    # 이것은 메인 GUI에 기능을 비활성화거나 화성화할때 사용되는 값.
    def CBValueSave(self):
        # 콤보박스의 아이템을 변경하는 경우 설정을 저장하는 기능.
        CBClickSave = False # 여기서 버튼을 눌러서 설정을 저장함. / Basic setting value: False
        # False 저장 로직 작성안됨, 작성 필요
        CBSetValueDict = {} # 임시 설정 저장

        if (self.AvoidDuplicateCreation["CBValueSave-Func"] == True) or (CBClickSave == False):
            print("Save button clicked - %s" % len(self.CBDict.values()))
            for Lable, combobox in self.CBDict.items():
                if CBClickSave:
                    combobox.currentTextChanged.connect(lambda text: print(text))
                else:
                    CBSetValueDict[Lable] = combobox.currentIndex()
            
            # 실시간 콤보박스 변경시 값
            if CBClickSave == True:
                # 중복 생성 방지를 위해 비활성
                self.AvoidDuplicateCreation["CBValueSave-Func"] = False
            
            # 그 외
            else:
                # 설정 불러오기 배열값 저장
                try:
                    SaveJSON(r"GUI\Settings\Settings.json", CBSetValueDict)
                    print("설정값이 저장됨.")
                
                except Exception as e:
                    print("CBValueSave Error:", e)
                    print("설정값 저장을 실패함.")


        # 여기 else 에 저장 로직 작성 필요
        else:
            print("False value")