from PyQt5.QtCore import QThread, pyqtSignal
from Metal_HUD_parse import *

# 스레드
class PerformanceParsingThread(QThread):
    UpdateFileLabelSignal = pyqtSignal(str)
    ThreadFinishedSignal = pyqtSignal()

    def __init__(self, FileName, FileData, UnitConversion, DecimalPoint, parent=None):
        super().__init__(parent)
        self.FileName = FileName
        self.FileData = FileData
        self.UnitConversion = UnitConversion
        self.DecimalPoint = DecimalPoint
        
    # 성능 파싱 시작
    def run(self):
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Start...')
        DataSplit(self.FileData, PerformanceCalculationConditions, PerformanceData, PerformanceErrorData)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Loding...')
        ConverttoFPS(PerformanceData, PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        LastDataAvg(PerformanceData, PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Done!')
        
        # 스레드 종료
        self.ThreadFinishedSignal.emit()