from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QVBoxLayout, 
    QMainWindow, 
    QAction, 
    QToolBar, 
    QLabel, 
    QStyledItemDelegate, 
    QPushButton, 
    QGridLayout, 
    QComboBox
    )

from PyQt5.QtCore import Qt, QSize
from GUIStyle import *
from OpenJson import *


# 콤보박스 아이템간의 간격을 조절하는 클래스.
class CustomDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 40)


# 설정 화면을 구성하는 클래스
class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        # cb data
        self.CBDict = {}
        
        # 중복 생성 방지
        self.AvoidDuplicateCreation = {
            "CBValueSave-Func": True,
            "CBValueSave-FileSaved": None
        }
        
        super().__init__(parent)
        self.InitUI()

    # 기본 UI 초기화
    def InitUI(self):
        self.setWindowTitle("Settings")
        self.move(100, 100)
        self.setMinimumSize(600, 600)

        # UI 구현
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid = QGridLayout()
        grid.setVerticalSpacing(20) # 수직 간격 20
        central_widget.setLayout(grid)

        # 파라미터 정의 - 개발시 *.json 등으로 관리
        # 설정값이 불러와지지 않을 경우 경로 재설정 필요, 후에 OS 모듈등으로 자동으로 경로를 찾아주는 코드를 추가할 생각
        setSttings = OpenJson(r"GUI\Settings\Settings_LBL_CB.json")
        setButtons = OpenJson(r"GUI\Settings\Settings_BTN.json")
        BtnFuns = [self.CBValueSave, lambda: None, lambda: None, lambda: None]

        for index, (lable, items) in enumerate(setSttings.items()):
            self.AddGrid_Lbl_Cb(lable, items, grid, index)

            # 마지막에 버튼 추가함.
            ExistingIndex = index + 1 # 기존 인덱스 값 사용.
            if ExistingIndex == len(setSttings):
                self.AddGridBtn(ExistingIndex, grid, BtnFuns, setButtons)

    # 설정, 라벨 - 콤보박스
    def AddGrid_Lbl_Cb(self, lable, items, grid, index):
        lbl, cb = self.addLableComboBox(lable, *items)
        # 중복방지 lable
        self.CBDict[lable] = cb

        for obj_index, obj in enumerate([lbl, cb]):
            grid.addWidget(obj, index, obj_index)

    # 설정, 버튼
    def AddGridBtn(self, index, grid, BtnFuns, setButtons):
        BtnColindex = index
        BtnRowindex = 0
        for funs_index, (label, items) in enumerate(setButtons.items()):
            if BtnRowindex % 2 == 0 and BtnRowindex != 0:
                BtnColindex += 1
                BtnRowindex = 0
            
            SaveBtn = self.addBtn(label, BtnFuns[funs_index], items)
            grid.addWidget(SaveBtn, BtnColindex, BtnRowindex)
            BtnRowindex += 1

    # 정의된 라벨과 콤보박스를 추가하는 함수
    def addLableComboBox(self, lableName, tooltip_name, items):
        label = QLabel(lableName)
        LabelType, LabelObjID = "QLabel", "addLabel"
        label.setToolTip(tooltip_name)
        label.setObjectName(LabelObjID)
        label.setStyleSheet(LabelStyle(LabelType+"#"+LabelObjID, 22))
        label.setAlignment(Qt.AlignCenter)

        # 콤보박스 아이템간의 높이조절
        cb = QComboBox(self)
        cb.setItemDelegate(CustomDelegate(cb))
        cb.setMaximumSize(180, 40)
        cb.setStyleSheet(ComboBoxStyle())

        # 아이템 추가
        for item in items:
            cb.addItem(str(item))

        return label, cb
    
    # 정의된 버튼을 추가하는 함수
    def addBtn(self, name, fun, tooltip_name):
        button = QPushButton(name) 

        button.clicked.connect(fun)
        button.setMaximumSize(180, 80)
        # 툴팁
        button.setToolTip(tooltip_name)
        button_Type, button_ObjID = "QPushButton", "addBtn"
        button.setObjectName(button_ObjID)
        button.setStyleSheet(ButtonStyle(button_Type+"#"+button_ObjID))

        return button
    
    # 콤보박스의 선택된 값을 *.json 으로 저장함.
    # 이것은 메인 GUI에 기능을 비활성화거나 화성화할때 사용되는 값.
    def CBValueSave(self):
        # 콤보박스의 아이템을 변경하는 경우 설정을 저장하는 기능.
        CBClickSave = False # 여기서 버튼을 눌러서 설정을 저장함. / Basic setting value: False

        if (self.AvoidDuplicateCreation["CBValueSave-Func"] == True) or (CBClickSave == False):
            print("Save button clicked - %s" % len(self.CBDict.values()))
            for combobox in self.CBDict.values():
                if CBClickSave:
                    combobox.currentTextChanged.connect(lambda text: print(text))
                else:
                    print(combobox.currentIndex(), combobox.currentText())
            
            # 중복 생성 방지를 위해 비활성
            self.AvoidDuplicateCreation["CBValueSave-Func"] = False
        
        else:
            print("False value")



# 메인 GUI에 툴바를 구성하는 클래스
class SettingsToolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet(ToolbarStyle())

        # Settings button creation
        self.settings_action = QAction("Settings", self)
        self.settings_action.triggered.connect(self.show_settings)
        self.toolbar.addAction(self.settings_action)
        
        # Toolbar to layout
        self.layout.addWidget(self.toolbar)
        self.setLayout(self.layout)

    def show_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

if __name__ == "__main__":
    app = QApplication([])
    toolbar = SettingsToolbar()
    toolbar.show()
    app.exec_()
