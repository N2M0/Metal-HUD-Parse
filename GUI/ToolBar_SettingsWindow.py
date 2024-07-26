from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,  
    QLabel, 
    QStyledItemDelegate, 
    QPushButton, 
    QGridLayout, 
    QComboBox
    )

from PyQt5.QtCore import Qt, QSize
from GUIStyle import *
from Json_func import *
from Settings_JSON_Write import *
from ToolBar_OptionsHandler import *
from ToolBar_developer import *
from constant import *


# 콤보박스 아이템간의 간격을 조절하는 클래스.
class CustomDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 50)

# 설정 화면을 구성하는 클래스
class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        self._name = __class__.__name__
        
        # 특정 폴더에 있는 폰트 로드
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        # cb data
        self.CBDict = {}
        
        # 중복 생성 방지
        self.AvoidDuplicateCreation = {
            CBValueSave_Func: True,
            CBValueSave_FileSaved: True
        }
        
        super().__init__(parent)
        self.SettingsManager = OptionsHandler(self)
        self.developer = Developer(self)
        
        self.InitUI()
        self.SettingsManager.CBSetValueRead()

    # 기본 UI 초기화
    def InitUI(self):
        self.setWindowTitle("Settings")
        self.setMinimumSize(800, 600)
        self.resize(1000, 800)

        # UI 구현
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid = QGridLayout()
        grid.setVerticalSpacing(20) # 수직 간격 20
        central_widget.setLayout(grid)

        # 파라미터 정의 - 개발시 *.json 등으로 관리
        # 설정값이 불러와지지 않을 경우 경로 재설정 필요, 후에 OS 모듈등으로 자동으로 경로를 찾아주는 코드를 추가할 생각


        try:
            setSttings = OpenJson(SettingFilePath)
            setButtons = OpenJson(ButtonFilePath)

        except (FileNotFoundError, json.JSONDecodeError):
            # 기본 설정값 초기화
            SetSaved()

            setSttings = OpenJson(SettingFilePath)
            setButtons = OpenJson(ButtonFilePath)

        try:
            BtnFuns = [self.SettingsManager.CBValueSave, self.developer.show, lambda: None, lambda: None]

            for index, (lable, items) in enumerate(setSttings.items()):
                self.AddGrid_Lbl_Cb(lable, items, grid, index)

                # 마지막에 버튼 추가함.
                ExistingIndex = index + 1 # 기존 인덱스 값 사용.
                if ExistingIndex == len(setSttings):
                    self.AddGrid_Btn(ExistingIndex, grid, BtnFuns, setButtons)
                    
        except Exception as e:
            print(f"{self._name} - InitUI - 1 Error:", e)
            
    # 설정, 라벨 - 콤보박스
    def AddGrid_Lbl_Cb(self, lable, items, grid, index):
        try:
            lbl, cb = self.addLabelComboBox(lable, *items)
            # 중복방지 lable
            self.CBDict[lable] = cb

            for obj_index, obj in enumerate([lbl, cb]):
                grid.addWidget(obj, index, obj_index)
                
        except Exception as e:
            print(f"{self._name} - AddGrid_Lbl_Cb Error:", e)
            
    # 설정, 버튼
    def AddGrid_Btn(self, index, grid, BtnFuns, setButtons):
        try:
            BtnColindex = index
            BtnRowindex = 0
            for funs_index, (label, items) in enumerate(setButtons.items()):
                if BtnRowindex % 2 == 0 and BtnRowindex != 0:
                    BtnColindex += 1
                    BtnRowindex = 0
                
                SaveBtn = self.addBtn(label, BtnFuns[funs_index], items)
                grid.addWidget(SaveBtn, BtnColindex, BtnRowindex)
                BtnRowindex += 1
                
        except Exception as e:
            print(f"{self._name} - AddGrid_Btn Error:", e)

    # 정의된 라벨과 콤보박스를 추가하는 함수
    def addLabelComboBox(self, lableName, tooltip_name, items):
        try:
            label = QLabel(lableName)
            LabelType, LabelObjID = "QLabel", "addLabel"
            label.setToolTip(tooltip_name)
            label.setObjectName(LabelObjID)
            label.setStyleSheet(LabelStyle(LabelType+"#"+LabelObjID, self.font_family, 22))
            label.setAlignment(Qt.AlignCenter)

            # 콤보박스 아이템간의 높이조절
            cb = QComboBox(self)
            cb.setItemDelegate(CustomDelegate(cb))
            cb.setMaximumSize(380, 40)
            cb.setStyleSheet(ComboBoxStyle(self.font_family))

            # 아이템 추가
            for item in items:
                cb.addItem(str(item))

            return label, cb

        except Exception as e:
            print(f"{self._name} - addLabelComboBox Error:", e)
            return None, None
    
    # 정의된 버튼을 추가하는 함수
    def addBtn(self, name, fun, tooltip_name):
        try:
            button = QPushButton(name) 

            button.clicked.connect(fun)
            button.setMaximumSize(380, 100)
            # 툴팁
            button.setToolTip(tooltip_name)
            button_Type, button_ObjID = "QPushButton", "addBtn"
            button.setObjectName(button_ObjID)
            button.setStyleSheet(ButtonStyle(button_Type+"#"+button_ObjID, self.font_family))

            return button

        except Exception as e:
            print(f"{self._name} - addBtn Error:", e)
            return None

if __name__ == "__main__":
    app = QApplication([])
    _SettingsWindow = SettingsWindow()
    _SettingsWindow.show()
    app.exec_()