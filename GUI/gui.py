import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGridLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from Metal_HUD_parse import *
from gui_style import *
from gui_thread import *

class MetalHUDParse(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 윈도우 설정
        self.setWindowTitle('My PyQt5 Window')
        self.resize(1400, 800)
        
        # 레이아웃 생성
        Mainvbox = QVBoxLayout()
        
        # 파일 리드
        self.FileReadframe = self.FileReadWindow()
        Mainvbox.addWidget(self.FileReadframe)
        
        # 레이아웃 설정
        self.setLayout(Mainvbox)


    def FileReadWindow(self):
        FileReadframe = QFrame()
        FileReadframe.setFrameShape(QFrame.Panel | QFrame.Sunken)
        FileReadvbox = QVBoxLayout()
        
        # 파일 라벨 생성
        self.FileLabel = QLabel("Load The File.")
        FileLabelType, FileLabelObjID = "QLabel", "FileLabel"
        self.FileLabel.setObjectName(FileLabelObjID)
        self.FileLabel.setStyleSheet(FileLabelStyle(FileLabelType+"#"+FileLabelObjID))
        self.FileLabel.setAlignment(Qt.AlignCenter)
        
        # 파일 버튼 생성
        self.FileReadBtn = QPushButton('File Read')
        FileButtonType, FileButtonObjID = "QPushButton", "FileReadBtn"
        self.FileReadBtn.setObjectName(FileButtonObjID)
        self.FileReadBtn.setStyleSheet(FileReadBtnStyle(FileButtonType+"#"+FileButtonObjID))
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
        FileName, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if FileName:
            self.FileLabel.setText(f'Selected File: {FileName}')
            self.StartParsePerformance(FileName)
    
    def StartParsePerformance(self, FileName):
        self.thread = PerformanceParsingThread(FileName)
        self.thread.UpdateFileLabelSignal.connect(lambda text: self.FileLabel.setText(text))
        self.thread.ThreadFinishedSignal.connect(lambda: QTimer.singleShot(1000, self.FileReadframe.hide))
        self.thread.start()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MetalHUDParse()
    window.show()
    sys.exit(app.exec_())
