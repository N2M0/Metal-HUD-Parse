from PyQt5.QtWidgets import QWidget, QMessageBox
from GUIStyle import *
from GUIThread import *

class ParsedDataSavedWorker(QWidget):
    def __init__(self, parent):
        super(ParsedDataSavedWorker, self).__init__(parent)
        self._name = __class__.__name__
        
        self.parent = parent
    
    # parent 연결 주의
    def start(self):
        try:
            self.SaveThread = PerformanceParsingResultsSaveThread(parent=self.parent)
            self.SaveThread.MsgBoxNotifications.connect(self.ShowMessagebox)
            self.SaveThread.start()
            
        except Exception as e:
            print(f"{self._name} - start Error:", e)
            
    # 메시지박스
    def ShowMessagebox(self, setText):
        try:
            msgBox = QMessageBox(parent=self.parent)
            msgBox.setWindowTitle('Parsed Notifications')
            msgBox.setText(setText)
            
            # 스타일 시트 설정
            msgBox.setStyleSheet(MsgBoxStyle())
            msgBox.exec_()
        
        except Exception as e:
            print(f"{self._name} - ShowMessagebox Error:", e)
            