from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QVBoxLayout, 
    QAction, 
    QToolBar, 
    )

from GUIStyle import *
from ToolBar_SettingsWindow import *


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
