from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtGui
from GUIStyle import *
from GUIThread import *
from constant import *
from applog import *

logger = InitLogger()


class ParsedDataSavedWorker(QWidget):
    def __init__(self, parent):
        super(ParsedDataSavedWorker, self).__init__(parent)
        self._name = __class__.__name__
        
        # 특정 폴더에 있는 폰트 로드
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        
        self.parent = parent
    
    # parent 연결 주의
    def start(self):
        try:
            self.SaveThread = PerformanceParsingResultsSaveThread(parent=self.parent)
            self.SaveThread.MsgBoxNotifications.connect(self.ShowMessagebox)
            self.SaveThread.start()
            
        except Exception as e:
            logger.error(f"{self._name} - start Error: {e}")
            
    # 메시지박스
    def ShowMessagebox(self, setText):
        try:
            msgBox = QMessageBox(parent=self.parent)
            msgBox.setWindowTitle('Parsed Notifications')
            msgBox.setText(setText)
            
            # 스타일 시트 설정
            msgBox.setStyleSheet(MsgBoxStyle(self.font_family))
            msgBox.exec_()
            
            # Error 텍스트 포함시 강제 종료
            if "Error:" in setText:
                sys.exit(1)
        
        except Exception as e:
            logger.error(f"{self._name} - ShowMessagebox Error: {e}")
            