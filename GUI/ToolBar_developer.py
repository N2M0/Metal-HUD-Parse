from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QGridLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout
    )
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from GUIStyle import *
from Json_func import *
from Settings_JSON_Write import *
from constant import *
from applog import *

logger = InitLogger(CurrentFileName(__file__))


developers = {
    "Square-Dream": {
        "tooltip": "네모난꿈",
        "developed": {
            "tooltip": "개발한 것",
            "working": "Back-End (Calculation Formulas • Parsing)"
        }
    },
    
    "Home-Gravity": {
    "tooltip": "집-중력",
    "developed": {
        "tooltip": "개발한 것",
        "working": "Front-End (Graphical User Interface)"
    }
}
}

# 만든이
class Developer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._name = __class__.__name__
        
        # 특정 폴더에 있는 폰트 로드
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        self.InitUI()

    def InitUI(self):
        try:
            self.setWindowTitle("Developers")
            self.setMinimumSize(700, 400)

            # UI 구현
            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            vbox = QVBoxLayout()
            grid = QGridLayout()
            grid.setVerticalSpacing(50) # 수직 간격 50
            central_widget.setLayout(vbox)
            
            # 상단 중앙 라벨
            Developers_label = self.add_Label("Developers", "개발자들")
            self.add_grid_layout(grid)
            self.addlayout(vbox, Developers_label, grid)
            
        except Exception as e:
            logger.error(f"{self._name} - 개발자 화면을 초기화하는 과정에 문제가 생겼습니다. | Error Code: {e}")

    def addlayout(self, vbox, Developers_label, grid):
        try:
            vbox.addSpacing(20)
            vbox.addWidget(Developers_label)
            vbox.addStretch(1)
            vbox.addSpacing(10)
            vbox.addLayout(grid)
            vbox.addStretch(3)
            
        except Exception as e:
            logger.error(f"{self._name} - 개발자 화면을 구성하는 메인 레이아웃에 서브(그리드) 레이아웃 또는 위젯을 추가하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            
    def add_grid_layout(self, grid):
        try:
            col, row = 0, 0
            
            for key, value in developers.items():
                for label_text, tooltip in [(key, value["tooltip"]), 
                                            (value["developed"]["working"], 
                                            value["developed"]["tooltip"])]:
                    
                    if row % 2 != 0: # 홀수 행일 때
                        color = "rgb(58, 134, 255)"
                    
                    else:
                        color = "rgb(0, 0, 0)"
                    
                    label = self.add_Label(label_text, tooltip, color)
                    grid.addWidget(label, col, row)
                    
                    row += 1
                    if row % 2 == 0:
                        row = 0
                        col += 1
                        
        except Exception as e:
            logger.error(f"{self._name} - 개발자 화면을 구성하는 서브(그리드) 레이아웃에 위젯을 추가하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            
    def add_Label(self, lableName, tooltip_name=None, color="black"):
        try:
            label = QLabel(lableName)
            LabelType, LabelObjID = "QLabel", "addLabel"
            label.setToolTip(tooltip_name)
            label.setObjectName(LabelObjID)
            label.setStyleSheet(LabelStyle(LabelType+"#"+LabelObjID, self.font_family, 22, color))
            label.setAlignment(Qt.AlignCenter)
            
            return label
        
        except Exception as e:
            logger.error(f"{self._name} - 개발자 화면을 구성하는 서브(그리드) 레이아웃에 추가하는 레이블 위젯 함수의 문제가 생겼습니다. | Error Code: {e}")
            
            
            
            
if __name__ == "__main__":
    app = QApplication([])
    _developer = Developer()
    _developer.show()
    app.exec_()