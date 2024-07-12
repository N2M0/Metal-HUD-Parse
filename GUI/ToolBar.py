from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QAction, QMenu, QToolBar, QLabel, QStyledItemDelegate, QPushButton, QGridLayout, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from GUIStyle import *

# 콤보박스의 아이템간의 간격을 조절하는 클래스.
class CustomDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 40)

# 설정 화면을 구성하는 클래스
class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 600, 600)

        # UI 구현
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid = QGridLayout()
        grid.setVerticalSpacing(20) # 수직 간격 20
        central_widget.setLayout(grid)


        # 파라미터 정의
        setSttings = {
            "Preview data": ("테이블 미리보기 여부", ["Test1", "test2"]),
            "Startup mode": ("시작시 모드 여부", ["Test1", "Test3", "Test4"]),
            "test1": ("test1", ["Test1", "Test3", "Test4"]),
            "test2": ("test2", ["Test1", "Test3", "Test4"]),
            "test3": ("test3", ["Test1", "Test3", "Test4"]),
            
        }

        setButton = {
            "Save": (lambda: None, "설정을 저장합니다."),
            "Next": (lambda: None, "Next합니다."),
            "END": (lambda: None, "END합니다."),
            "Home": (lambda: None, "Home합니다.")
            
        }

        for index, (lable, items) in enumerate(setSttings.items()):
            lbl, cb = self.addLableComboBox(lable, *items)
            for obj_index, obj in enumerate([lbl, cb]):
                grid.addWidget(obj, index, obj_index)

            # 마지막에 버튼 추가함.
            if index + 1 == len(setSttings):
                BtnColindex = index + 1
                BtnRowindex = 0
                for index, (label, items) in enumerate(setButton.items()):
                    if BtnRowindex % 2 == 0 and BtnRowindex != 0:
                        BtnColindex += 1
                        BtnRowindex = 0
                    
                    SaveBtn = self.addBtn(label, *items)
                    grid.addWidget(SaveBtn, BtnColindex, BtnRowindex)
                    BtnRowindex += 1

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
        cb.setFixedSize(180, 40)
        cb.setStyleSheet(ComboBoxStyle())

        # 아이템 추가
        for item in items:
            cb.addItem(str(item))

        return label, cb
    
    def addBtn(self, name, fun, tooltip_name):
        button = QPushButton(name)
        button.clicked.connect(fun)
        button.setFixedSize(180, 80)
        # 툴팁
        button.setToolTip(tooltip_name)
        button_Type, button_ObjID = "QPushButton", "addBtn"
        button.setObjectName(button_ObjID)
        button.setStyleSheet(ButtonStyle(button_Type+"#"+button_ObjID))

        return button

    def save_settings(self):
        # 설정 값 저장 코드 작성
        print(f"Option 1: {self.option1_edit.text()}")
        print(f"Option 2: {self.option2_edit.text()}")
        self.close()


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
