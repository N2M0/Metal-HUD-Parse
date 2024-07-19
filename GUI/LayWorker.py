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
        try:
            self.ParsingThread = PerformanceParsingThread(self.parent, self.FileName, self.FileData, self.benchmarkBasedTime, self.UnitConversion, self.DecimalPoint)
            self.ParsingThread.UpdateFileLabelSignal.connect(lambda text: self.StartPerformanceLable.setText(text))
            self.ParsingThread.EmitInitializeTableSignal.connect(self.InitializeTable)
            self.ParsingThread.EmitParsedSignal.connect(self.UpdateTable)
            self.ParsingThread.EmitParsedPbarSignal.connect(self.UpdateProgressBar)
            self.ParsingThread.ThreadFinishedSignal.connect(self.ParsedResultsTable.resizeColumnsToContents)
            self.ParsingThread.start()
            
        except Exception as e:
            print("LayUpdateWorker - start Error:", e)

    # 테이블 초기화
    def InitializeTable(self, label_list, col_count, row_count):
        try:
            self.ParsedResultsTable.setColumnCount(0)    
            self.ParsedResultsTable.setRowCount(0)
            self.ParsedResultsTable.setColumnCount(col_count)
            self.ParsedResultsTable.setRowCount(row_count)
            self.ParsedResultsTable.setHorizontalHeaderLabels(label_list)
        except Exception as e:
            print("LayUpdateWorker - InitializeTable Error:", e)
            
    # 테이블 업데이트 함수
    def UpdateTable(self, col, row, value):
        try:
            # 테이블에 데이터를 추가
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)  # 텍스트 정렬 (옵션)
            self.ParsedResultsTable.setItem(row, col, item)

        except Exception as e:
            print("LayUpdateWorker - UpdateTable Error:", e)

    # 프로그래스바 업데이트 함수
    def UpdateProgressBar(self, sum_pbar, sum_count):
        try:
            progress = (sum_pbar / sum_count) * 100  # 프로그래스바 계산
            self.ParsedPbar.setValue(int(progress))  # 프로그래스바 업데이트

        except Exception as e:
            print("LayUpdateWorker - UpdateProgressBar Error:", e)