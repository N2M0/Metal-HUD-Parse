from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QAction, QMenu, QToolBar, QLabel, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from GUIStyle import *

class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 300)

        # UI 구현
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        central_widget.setLayout(layout)

        # 설정 옵션 추가
        label1 = QLabel("Option 1:")
        self.option1_edit = QLineEdit()
        self.option1_edit.setPlaceholderText("준비중인 기능")
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.option1_edit, 0, 1)

        label2 = QLabel("Option 2:")
        self.option2_edit = QLineEdit()
        self.option2_edit.setPlaceholderText("준비중인 기능")
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.option2_edit, 1, 1)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button, 2, 1)

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
