from PyQt5.QtWidgets import QWidget, QMessageBox
from GUIStyle import *
from GUIThread import *

class ParsedDataSavedWorker(QWidget):
    def __init__(self, parent):
        super(ParsedDataSavedWorker, self).__init__(parent)
        self.parent = parent
    
        
    # parent 연결 주의
    def SavedStart(self):
        self.SaveThread = PerformanceParsingResultsSaveThread(parent=self.parent)
        self.SaveThread.MsgBoxNotifications.connect(self.ShowMessagebox)
        self.SaveThread.start()
        self.SaveThread.wait()
        
    # 메시지박스
    def ShowMessagebox(self, setText):
        msgBox = QMessageBox(parent=self.parent)
        msgBox.setWindowTitle('Parsed Notifications')
        msgBox.setText(setText)
        
        # 스타일 시트 설정
        msgBox.setStyleSheet(MsgBoxStyle())
        msgBox.exec_()