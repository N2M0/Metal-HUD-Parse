from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from GUIStyle import *
from GUIThread import *
import sys
from applog import *

logger = InitLogger()


# 메인 레이아웃을 업데이트 하기 위한 클래스
class LayUpdateWorker(QWidget):
    def __init__(self, parent, FileName, benchmarkBasedTime, DecimalPoint):
        super(LayUpdateWorker, self).__init__(parent)
        self._name = __class__.__name__
        
        self.parent = parent
        self.StartPerformanceLable = self.parent.StartPerformanceLable
        self.ParsedResultsTable = self.parent.ParsedResultsTable
        self.ParsedPbar = self.parent.ParsedPbar
        self.ParseStartBtn = self.parent.ParseStartBtn
        
        # 인스턴스 변수
        self.FileName = FileName
        self.benchmarkBasedTime = benchmarkBasedTime
        self.DecimalPoint = DecimalPoint
    
    # 스레드 객체 생성
    def start(self):
        try:
            # 0 index parameter parent
            self.ParsingThread = PerformanceParsingThread(self.parent, self.FileName, self.benchmarkBasedTime, self.DecimalPoint)
            self.ParsingThread.ParseStartBtnState.connect(lambda x: self.ParseStartBtn.setEnabled(x))
            self.ParsingThread.UpdateFileLabelSignal.connect(lambda text: self.StartPerformanceLable.setText(text))
            self.ParsingThread.EmitTableState.connect(self.TableState)
            self.ParsingThread.EmitPbarState.connect(self.PbarState)
            self.ParsingThread.EmitInitializeTableSignal.connect(self.InitializeTable)
            self.ParsingThread.EmitParsedSignal.connect(self.UpdateTable)
            self.ParsingThread.EmitParsedPbarSignal.connect(self.UpdateProgressBar)
            self.ParsingThread.ThreadFinishedSignal.connect(self.ParsedResultsTable.resizeColumnsToContents)
            self.ParsingThread.start()
            
        except Exception as e:
            logger.error(f"{self._name} - start Error: {e}")

    def TableState(self, state):
        if state == True:
            self.ParsedResultsTable.show()
        
        else:
            self.ParsedResultsTable.hide()
        
    def PbarState(self, state):
        if state == True:
            self.ParsedPbar.show()
        
        else:
            self.ParsedPbar.hide()
        
    # 테이블 초기화
    def InitializeTable(self, label_list, col_count, row_count):
        try:
            self.ParsedResultsTable.setColumnCount(0)    
            self.ParsedResultsTable.setRowCount(0)
            self.ParsedResultsTable.setColumnCount(col_count)
            self.ParsedResultsTable.setRowCount(row_count)
            self.ParsedResultsTable.setHorizontalHeaderLabels(label_list)
            
        except Exception as e:
            logger.error(f"{self._name} - InitializeTable Error: {e}")
            
            
    # 테이블 업데이트 함수
    def UpdateTable(self, col, row, value):
        try:
            # 테이블에 데이터를 추가
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)  # 텍스트 정렬 (옵션)
            self.ParsedResultsTable.setItem(row, col, item)

        except Exception as e:
            logger.error(f"{self._name} - UpdateTable Error: {e}")
            sys.exit(1)

    # 프로그래스바 업데이트 함수
    def UpdateProgressBar(self, sum_pbar, sum_count):
        try:
            progress = (sum_pbar / sum_count) * 100  # 프로그래스바 계산
            self.ParsedPbar.setValue(int(progress))  # 프로그래스바 업데이트

        except Exception as e:
            logger.error(f"{self._name} - UpdateProgressBar Error: {e}")
            sys.exit(1)