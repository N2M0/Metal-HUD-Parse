from Metal_HUD_parse import  *
# import numpy as np

# 성능 데이터
# def PerformanceData():
#     return {
#         FPSData: list(range(1, 99999, 1)), # 프레임타임을 FPS로 바꾼 것
#         frameTimeData:list(range(1, 99999, 1)), # 프레임타임 데이터 (ms)
#         gpuTimeData:list(range(1, 99999, 1)), # GPU타임 데이터 (ms)
#         memoryData:list(range(1, 99999, 1)) # 메모리 사용량 저장
#     }

# # 딕셔너리 초기화
_PerformanceCalculationConditions = PerformanceCalculationConditions()

_PerformanceData = PerformanceData()
_PerformanceErrorData = PerformanceErrorData()

# 성능 데이터 분리
DataSplit(DataReader("output.csv"), _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData)

# FrameTime > FPS 변환
ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, 1000, 2)
# 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, 1000, 2)

# # 성능 데이터 분리
# DataSplit(DataReader("output.csv"), _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData)

# # FrameTime > FPS 변환
# ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, 1000, 2)
# # 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
# LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, 1000, 2)

import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer

class DataLoaderThread(QThread):
    data_loaded = pyqtSignal(int, int, str)

    def __init__(self, performance_data):
        super().__init__()
        self.performance_data = performance_data

    def run(self):
        for col, key in enumerate(self.performance_data):
            for row, value in enumerate(self.performance_data[key]):
                print(row, value)
                self.data_loaded.emit(row, col, str(value))
                # self.msleep(50)  # 데이터를 추가하는 사이에 짧은 지연을 추가하여 UI가 멈추지 않도록 함

class PerformanceDataTable(QWidget):
    def __init__(self, performance_data):
        super().__init__()
        self.initUI()
        self.load_data(performance_data)

    def initUI(self):
        self.table_widget = QTableWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)
        self.setWindowTitle('Performance Data')
        self.setGeometry(300, 100, 800, 600)

    def load_data(self, performance_data):
        # 데이터에 맞게 테이블 크기 설정
        row_count = max(len(v) for v in performance_data.values())
        col_count = len(performance_data)
        self.table_widget.setRowCount(row_count)
        self.table_widget.setColumnCount(col_count)
        self.table_widget.setHorizontalHeaderLabels(list(performance_data.keys()))

        # 데이터 로더 스레드 초기화 및 시작
        self.loader_thread = DataLoaderThread(performance_data)
        self.loader_thread.data_loaded.connect(self.add_data)
        self.loader_thread.start()

    def add_data(self, row, col, value):
        # 테이블에 데이터를 추가
        item = QTableWidgetItem(value)
        item.setTextAlignment(Qt.AlignCenter)  # 텍스트 정렬 (옵션)
        self.table_widget.setItem(row, col, item)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    table = PerformanceDataTable(_PerformanceData)
    table.show()
    sys.exit(app.exec_())

