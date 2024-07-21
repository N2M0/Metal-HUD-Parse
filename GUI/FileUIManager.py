from PyQt5.QtWidgets import  QFileDialog, QDesktopWidget
from PyQt5.QtCore import QTimer
from Metal_HUD_parse import *
from GUIStyle import *

# 메인 GUI 에서 파일 관련을 관리 및 구성하는 클래스 
class FileUIManager:
    def __init__(self, parent):
        self._name = __class__.__name__
        
        self.parent = parent
        self.FileLabel = parent.FileLabel
        self.FileReadframe = parent.FileReadframe
        self.Mainvbox = parent.Mainvbox
        self.StartPerformanceWindow = parent.StartPerformanceWindow

    # 파싱할 파일을 불러오는 함수
    def FileRead(self):
        try:
            options = QFileDialog.Options()
            self.FileName, _ = QFileDialog.getOpenFileName(self.parent, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
            if self.FileName:
                self.FileLabel.setText(f'Selected File: "{self.FileName}"')
                # Parent 로 받은 객체를 비동기적으로 1000ms (1초) 멈춤
                QTimer.singleShot(1000, self.FileReadframe.deleteLater)
                
                # StartPerformanceWindow 레이아웃 초기화
                QTimer.singleShot(1000, lambda: self.Mainvbox.addWidget(self.StartPerformanceWindow(self.FileName)))
            
            # 실패했을때
            else:
                self.FileLabel.setText(f'Selected File: Failed.')
                
        except Exception as e:
            print(f"{self._name} - FileRead Error:", e)

        # 창 위치를 중앙에 배치하는 함수를 호출
        self.center()

    # 창 위치를 중앙에 배치
    def center(self):
        try:
            self.parent.setMinimumSize(1200, 900) # 창 크기 고정
            qr = self.parent.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.parent.move(qr.topLeft())
            
        except Exception as e:
            print(f"{self._name} - Center Error:", e)
    
    # 파싱할 파일을 변경하는 함수
    def FileChanged(self):
        try:
            options = QFileDialog.Options()
            newFileName, _ = QFileDialog.getOpenFileName(self.parent, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
            if newFileName:
                return newFileName
            
            # QFileDialog 에서 취소를 눌렀을때 기존 파일명을 리턴
            else:
                return self.FileName

        except Exception as e:
            print(f"{self._name} - FileChanged Error:", e)
            return None