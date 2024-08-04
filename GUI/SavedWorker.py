from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from GUIStyle import *
from GUIThread import *
from config_paths import *
from applog import *

logger = InitLogger(CurrentFileName(__file__))


class ParsedDataSavedWorker(QWidget):
    def __init__(self, parent):
        super(ParsedDataSavedWorker, self).__init__(parent)
        
        # 특정 폴더에 있는 폰트 로드
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        self.parent = parent
        self.ParsedSave = self.parent.ParsedSave
    
    # parent 연결 주의
    def start(self):
        try:
            logger.info(f"스레드가 생성 됐습니다.")
            
            self.SaveThread = PerformanceParsingResultsSaveThread(parent=self.parent)
            self.SaveThread.ParsedSaveBtnState.connect(lambda x: self.ParsedSave.setEnabled(x))
            self.SaveThread.MsgBoxNotifications.connect(self.ShowMessagebox)
            self.SaveThread.ThreadFinishedSignal.connect(lambda: self.stop("스레드가 종료 됐습니다."))
            self.SaveThread.start()
            
        except Exception as e:
            logger.error(f"데이터 저장 스레드를 생성하는 과정에서 문제가 생겼습니다. | Error Code: {e}")
            
    # 메시지박스
    def ShowMessagebox(self, setText):
        try:
            msgBox = QMessageBox(parent=self.parent)
            msgBox.setWindowTitle('Parse Notification')
            msgBox.setText(setText)
            
            # 스타일 시트 설정
            msgBox.setStyleSheet(MsgBoxStyle(self.font_family))
            msgBox.exec_()
            
            # Error 텍스트 포함시 강제 종료
            if "Error:" in setText:
                sys.exit(1)
        
        except Exception as e:
            logger.error(f"데이터 저장 스레드의 메시지박스를 실행하는 과정에 생겼습니다. | Error Code: {e}")

    # 종료
    def stop(self, text):
        # 스레드 종료
        logger.info(text)
        self.Thread_stop()
        
        # 서브 클래스 종료
        self.deleteLater()
        

    def Thread_stop(self):
        # self.SaveThread.requestInterruption()
        self.SaveThread.quit()    # 이벤트 루프 종료
        self.SaveThread.wait()    # 스레드가 종료될 때까지 대기
        self.SaveThread.deleteLater()  # 안전하게 삭제 예약