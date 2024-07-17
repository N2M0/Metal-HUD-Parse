from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer, Qt
from GUIStyle import *
from GUIThread import *

# 메인 레이아웃을 업데이트 하기 위한 클래스, 코드의 가독성을 위해 클래스로 분리함.
class LayUpdateWorker(QWidget):
    def __init__(self, parent, FileName, FileData, benchmarkBasedTime, UnitConversion, DecimalPoint):
        super(LayUpdateWorker, self).__init__(parent)
        self.parent = parent
        self.StartPerformanceLable = self.parent.StartPerformanceLable
        self.ParsedResultsTable = self.parent.ParsedResultsTable
        self.ParsedPbar = self.parent.ParsedPbar
        
        # 인스턴스 변수
        self.FileName = FileName
        self.FileData = FileData
        self.benchmarkBasedTime = benchmarkBasedTime
        self.UnitConversion = UnitConversion
        self.DecimalPoint = DecimalPoint
    
    # 스레드 객체 생성
    def start(self):
        self.thread = PerformanceParsingThread(self.parent, self.FileName, self.FileData, self.benchmarkBasedTime, self.UnitConversion, self.DecimalPoint)
        self.thread.UpdateFileLabelSignal.connect(lambda text: self.StartPerformanceLable.setText(text))
        self.thread.EmitInitializeTableSignal.connect(self.InitializeTable)
        self.thread.EmitParsedSignal.connect(self.UpdateTable)
        self.thread.EmitParsedPbarSignal.connect(self.UpdateProgressBar)
        self.thread.ThreadFinishedSignal.connect(lambda: QTimer.singleShot(1000, self.UpdateTableResizeContents))
        self.thread.start()

    # 테이블 초기화
    def InitializeTable(self, label_list, col_count, row_count):
        self.ParsedResultsTable.setColumnCount(0)    
        self.ParsedResultsTable.setRowCount(0)
        self.ParsedResultsTable.setColumnCount(col_count)
        self.ParsedResultsTable.setRowCount(row_count)
        self.ParsedResultsTable.setHorizontalHeaderLabels(label_list)
        
    # 테이블 업데이트 함수
    def UpdateTable(self, col, row, value):
        # 테이블에 데이터를 추가
        item = QTableWidgetItem(value)
        item.setTextAlignment(Qt.AlignCenter)  # 텍스트 정렬 (옵션)
        self.ParsedResultsTable.setItem(row, col, item)
    
    def UpdateTableResizeContents(self):
        # 테이블 전체 크기 조정
        self.ParsedResultsTable.resizeColumnsToContents() # 행
        self.ParsedResultsTable.resizeRowsToContents() # 열 

    # 프로그래스바 업데이트 함수
    def UpdateProgressBar(self, sum_pbar, sum_count):
        progress = (sum_pbar / sum_count) * 100  # 프로그래스바 계산
        self.ParsedPbar.setValue(int(progress))  # 프로그래스바 업데이트
        