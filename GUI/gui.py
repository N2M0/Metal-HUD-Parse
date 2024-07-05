import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGridLayout, QFrame
from PyQt5.QtCore import Qt
from Metal_HUD_parse import *
from gui_style import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 윈도우 설정
        self.setWindowTitle('My PyQt5 Window')
        self.resize(800, 800)
        
        # 레이아웃 생성
        Mainvbox = QVBoxLayout()
        
        # 파일리드
        FileReadframe = self.FileReadWindow()
        Mainvbox.addWidget(FileReadframe)
        
        # 레이아웃 설정
        self.setLayout(Mainvbox)

    def FileReadWindow(self):
        FileReadframe = QFrame()
        FileReadframe.setFrameShape(QFrame.Panel | QFrame.Sunken)
        FileReadvbox = QVBoxLayout()
        
        # 파일 라벨 생성성
        self.FileLabel = QLabel("파일을 불러옵니다.")
        FileLabelType, FileLabelObjID = "QLabel", "FileLabel"
        self.FileLabel.setObjectName(FileLabelObjID)
        self.FileLabel.setStyleSheet(FileLabelStyle(FileLabelType+"#"+FileLabelObjID))
        self.FileLabel.setAlignment(Qt.AlignCenter)
        
        # 버튼 생성
        self.FileReadBtn = QPushButton('파일 열기')
        self.FileReadBtn.setFixedSize(200, 80)
        self.FileReadBtn.clicked.connect(self.FileRead)

        # 라벨과 버튼을 중앙에 배치
        FileReadvbox.addStretch(1)
        FileReadvbox.addWidget(self.FileLabel, alignment=Qt.AlignCenter)
        FileReadvbox.addSpacing(20)  # 라벨과 버튼 사이의 여백
        FileReadvbox.addWidget(self.FileReadBtn, alignment=Qt.AlignCenter)
        FileReadvbox.addStretch(1)
        
        FileReadframe.setLayout(FileReadvbox)
        
        
        return FileReadframe
    
    # 파일 불러오기
    def FileRead(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            self.FileLabel.setText(f'Selected File: {fileName}')

    # 성능 파싱 시작
    def StartParsePerformance(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
