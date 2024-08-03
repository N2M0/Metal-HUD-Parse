from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from GUIStyle import *
from GUIThread import *
import sys
from applog import *

logger = InitLogger(CurrentFileName(__file__))


# 메인 레이아웃을 업데이트 하기 위한 클래스
class LayUpdateWorker(QWidget):
    def __init__(self, parent, FileName, benchmarkBasedTime, DecimalPoint):
        super(LayUpdateWorker, self).__init__(parent)
        
        # 변수
        self.parent = parent
        self.StartPerformanceLable = self.parent.StartPerformanceLable
        self.ParsedResultsTable = self.parent.ParsedResultsTable
        self.ParsedPbar = self.parent.ParsedPbar
        self.ParseStartBtn = self.parent.ParseStartBtn
        self.ParseStopBtn = self.parent.ParseStopBtn
        
        # 함수
        self.button_Hide = self.parent.button_Hide
        
        # 인스턴스 변수
        self.FileName = FileName
        self.benchmarkBasedTime = benchmarkBasedTime
        self.DecimalPoint = DecimalPoint
    
    # 스레드 객체 생성
    def start(self):
        try:
            logger.info(f"스레드가 생성 됐습니다.")
            
            # 종료 버튼 활성화
            self.button_Hide(self.ParseStopBtn, True, (10 ,20), (10 ,20), (10 ,20))
            
            # 스레드 시그널에 함수 연결
            self.ParsingThread = PerformanceParsingThread(self.parent, self.FileName, self.benchmarkBasedTime, self.DecimalPoint)
            self.ParsingThread.ParseStartBtnState.connect(lambda x: self.ParseStartBtn.setEnabled(x))
            self.ParsingThread.UpdateFileLabelSignal.connect(lambda text: self.StartPerformanceLable.setText(text))
            self.ParsingThread.EmitTableState.connect(self.StateChanged)
            self.ParsingThread.EmitPbarState.connect(self.StateChanged)
            self.ParsingThread.EmitInitializeTableSignal.connect(self.InitializeTable)
            self.ParsingThread.EmitParsedSignal.connect(self.UpdateTable)
            self.ParsingThread.EmitParsedPbarSignal.connect(self.UpdateProgressBar)
            self.ParsingThread.EmitTableResize.connect(self.ParsedResultsTable.resizeColumnsToContents)
            self.ParsingThread.ThreadFinishedSignal.connect(lambda : self.stop("스레드가 종료 됐습니다."))
            self.ParsingThread.start()
            
        except Exception as e:
            logger.error(f"Parse 스레드를 생성하는 과정에 문제가 생겼습니다. | Error Code: {e}")

    def StateChanged(self, state, obj):
        obj.setVisible(state)
        
    # 테이블 초기화
    def InitializeTable(self, label_list, col_count, row_count):
        try:
            self.ParsedResultsTable.setColumnCount(0)    
            self.ParsedResultsTable.setRowCount(0)
            self.ParsedResultsTable.setColumnCount(col_count)
            self.ParsedResultsTable.setRowCount(row_count)
            self.ParsedResultsTable.setHorizontalHeaderLabels(label_list)
            
        except Exception as e:
            logger.error(f"미리보기 테이블 초기값을 설정하는 데에 문제가 생겼습니다. | Error Code: {e}")
            
            
    # 테이블 업데이트 함수
    def UpdateTable(self, col, row, value):
        try:
            # 테이블에 데이터를 추가
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)  # 텍스트 정렬 (옵션)
            self.ParsedResultsTable.setItem(row, col, item)

        except Exception as e:
            logger.error(f"미리보기 테이블에 값을 업데이트하는 중에 문제가 생겼습니다. | Error Code: {e}")
            sys.exit(1)

    # 프로그래스바 업데이트 함수
    def UpdateProgressBar(self, sum_pbar, sum_count):
        try:
            progress = (sum_pbar / sum_count) * 100  # 프로그래스바 계산
            self.ParsedPbar.setValue(int(progress))  # 프로그래스바 업데이트

        except Exception as e:
            logger.error(f"프로그래스바를 업데이트하는 중에 문제가 생겼습니다. | Error Code: {e}")
            sys.exit(1)
    
    # 종료
    def stop(self, text):
        # 스레드 종료
        logger.info(text)
        self.Thread_stop()
        
        # 버튼 숨기기
        self.button_Hide(self.ParseStopBtn, False, (0 ,0), (10 ,20), (10 ,20))
        
        # 서브 클래스 종료
        self.deleteLater()
        

    def Thread_stop(self):
        self.ParsingThread.requestInterruption()
        self.ParsingThread.quit()    # 이벤트 루프 종료
        self.ParsingThread.wait()    # 스레드가 종료될 때까지 대기
        self.ParsingThread.deleteLater()  # 안전하게 삭제 예약
        