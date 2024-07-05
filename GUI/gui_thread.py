from PyQt5.QtCore import QThread, pyqtSignal
from Metal_HUD_parse import *

# 스레드
class PerformanceParsingThread(QThread):
    UpdateFileLabelSignal = pyqtSignal(str)
    ThreadFinishedSignal = pyqtSignal()

    def __init__(self, FileName, parent=None):
        super().__init__(parent)
        self.FileName = FileName  
        
    # 성능 파싱 시작
    def run(self):
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Start...')
        DataSplit(DataReader(self.FileName), PerformanceCalculationConditions, PerformanceData, PerformanceErrorData)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Loding...')
        ConverttoFPS(PerformanceData, PerformanceCalculationConditions, 1000, 2)
        LastDataAvg(PerformanceData, PerformanceCalculationConditions, 1000, 2)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Done!')
        
        # 스레드 종료
        self.ThreadFinishedSignal.emit()