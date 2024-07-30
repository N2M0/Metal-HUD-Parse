from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QVBoxLayout, 
    QAction, 
    QToolBar, 
    )
from PyQt5 import QtGui

from GUIStyle import *
from ToolBar_SettingsWindow import *
from constant import *
from applog import *

logger = InitLogger(CurrentFileName(__file__))

# 메인 GUI에 툴바를 구성하는 클래스
class SettingsToolbar(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._name = __class__.__name__
        
        # 특정 폴더에 있는 폰트 로드
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        
        self.InitUI()

    def InitUI(self):
        try:
            self.layout = QVBoxLayout()
            self.toolbar = QToolBar()
            self.toolbar.setStyleSheet(ToolbarStyle(self.font_family))

            # Settings button creation
            self.settings_action = QAction("Settings", self)
            self.settings_action.triggered.connect(self.show_settings)
            self.toolbar.addAction(self.settings_action)
            
            # Toolbar to layout
            self.layout.addWidget(self.toolbar)
            self.setLayout(self.layout)
            
        except Exception as e:
            logger.error(f"{self._name} - 툴바 버튼을 초기화하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            
    def show_settings(self):
        try:
            self.settings_window = SettingsWindow(self)
            self.settings_window.show()
            
        except Exception as e:
            logger.error(f"{self._name} - 설정 화면을 오픈하는 중에 문제가 생겼습니다. | Error Code: {e}")
            
if __name__ == "__main__":
    app = QApplication([])
    toolbar = SettingsToolbar()
    toolbar.show()
    app.exec_()
