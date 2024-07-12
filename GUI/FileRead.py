from PyQt5.QtWidgets import  QFileDialog
from PyQt5.QtCore import QTimer
from Metal_HUD_parse import *
from GUIStyle import *
from GUIThread import *

class FileReader:
    def __init__(self, parent):
        self.parent = parent
        self.FileLabel = parent.FileLabel
        self.FileReadframe = parent.FileReadframe
        self.Mainvbox = parent.Mainvbox
        self.StartPerformanceWindow = parent.StartPerformanceWindow

    # 파싱할 파일을 불러오는 함수
    def FileRead(self):
        options = QFileDialog.Options()
        self.FileName, _ = QFileDialog.getOpenFileName(self.parent, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if self.FileName:
            self.FileLabel.setText(f'Selected File: {self.FileName}')
            # Parent 로 받은 객체를 비동기적으로 1000ms (1초) 멈춤
            QTimer.singleShot(1000, self.FileReadframe.hide)
            
            # StartPerformanceWindow 레이아웃 초기화
            QTimer.singleShot(1000, lambda: self.Mainvbox.addWidget(self.StartPerformanceWindow(self.FileName)))
        
        # 실패했을때
        else:
            self.FileLabel.setText(f'Selected File: Failed.')

    # 파싱할 파일을 변경하는 함수
    def FileChanged(self):
        options = QFileDialog.Options()
        newFileName, _ = QFileDialog.getOpenFileName(self.parent, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if newFileName:
            return newFileName
        
        # QFileDialog 에서 취소를 눌렀을때 기존 파일명을 리턴
        else:
            return self.FileName