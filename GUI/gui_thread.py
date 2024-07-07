from PyQt5.QtCore import QThread, pyqtSignal
from Metal_HUD_parse import *
import numpy as np

# 스레드
class PerformanceParsingThread(QThread):
    UpdateFileLabelSignal = pyqtSignal(str)
    ThreadFinishedSignal = pyqtSignal()

    def __init__(self, FileName, FileData, benchmarkBasedTimeValue, UnitConversion, DecimalPoint, parent=None):
        super().__init__(parent)
        self.FileName = FileName
        self.benchmarkBasedTimeValue = benchmarkBasedTimeValue
        self.FileData = FileData
        self.UnitConversion = UnitConversion
        self.DecimalPoint = DecimalPoint
        
    # 성능 파싱 시작
    def run(self):
        # 딕셔너리 초기화
        _PerformanceCalculationConditions = PerformanceCalculationConditions()
        _PerformanceData = PerformanceData()
        _PerformanceErrorData = PerformanceErrorData()
        
        _PerformanceCalculationConditions[benchmarkBasedTime] = self.benchmarkBasedTimeValue
        
        
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Start...')
        DataSplit(self.FileData, _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Loding...')
        ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Done!')
        
        # pprint(_PerformanceData)
        pprint(np.mean(_PerformanceData[FPSData]))
        
        # 스레드 종료
        self.ThreadFinishedSignal.emit()