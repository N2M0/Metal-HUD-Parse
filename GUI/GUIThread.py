from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView, QHeaderView, QTableWidgetItem
from Metal_HUD_parse import *
import numpy as np
from GUIStyle import *

_PerformanceCalculationConditions = None
_PerformanceData = None
_PerformanceErrorData  = None

# 스레드
class PerformanceParsingThread(QThread):
    UpdateFileLabelSignal = pyqtSignal(str)
    EmitParsedSignal = pyqtSignal(list, int, int, int, int, int, int, str)  # 추가된 신호
    ThreadFinishedSignal = pyqtSignal()

    def __init__(self, FileName, FileData, benchmarkBasedTimeValue, UnitConversion, DecimalPoint, parent=None):
        super().__init__(parent)
        self.FileName = FileName
        self.benchmarkBasedTimeValue = benchmarkBasedTimeValue
        self.FileData = FileData
        self.UnitConversion = UnitConversion
        self.DecimalPoint = DecimalPoint
        
        self.parent = parent
        self.ParsedResultsTable = self.parent.ParsedResultsTable
        
    # 성능 파싱 시작
    def run(self):
        # 딕셔너리 초기화
        global _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData
        
        _PerformanceCalculationConditions = PerformanceCalculationConditions()
        _PerformanceData = PerformanceData()
        _PerformanceErrorData = PerformanceErrorData()

        _PerformanceCalculationConditions[benchmarkBasedTime] = self.benchmarkBasedTimeValue
        
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Start...')
        DataSplit(self.FileData, _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Loding...')
        ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        self.emitParsedSignal()
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Done!')
        
        
        # 스레드 종료
        self.ThreadFinishedSignal.emit()
    
    
    def emitParsedSignal(self):
        # 데이터에 맞게 테이블 크기 설정
        row_count = max(len(v) for v in _PerformanceData.values())
        sum_count = sum(len(v) for v in _PerformanceData.values())
        col_count = len(_PerformanceData)
        LabelList = list(_PerformanceData.keys())
        
        sum_pbar = 1 
        for col, key in enumerate(_PerformanceData):
            for row, value in enumerate(_PerformanceData[key]):
                self.EmitParsedSignal.emit(LabelList, sum_pbar, sum_count, col_count, row_count, col, row, str(value))
                sum_pbar += 1


class PerformanceParsingResultsSaveThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
    
    
    def ShowMessagebox(self, setText):
        msgBox = QMessageBox(self.parent)
        msgBox.setWindowTitle('Parsed Save')
        msgBox.setText(setText)
        
        # 스타일 시트 설정
        msgBox.setStyleSheet(MsgBoxStyle())
        msgBox.exec_()
    
    def run(self):
        if all([_PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData]):
            PerformanceCsvSave("FPS-Result.csv", f"FPS - 약 {_PerformanceCalculationConditions[benchmarkBasedTime]} ms마다 평균치 계산", _PerformanceData[FPSData])
            PerformanceCsvSave("Frametime-Result.csv", f"Frametime", _PerformanceData[frameTimeData])
            PerformanceCsvSave("GPUTime-Result.csv", f"GPUTime", _PerformanceData[gpuTimeData])
            PerformanceCsvSave("Memory-Result.csv", f"Memory(MB)", _PerformanceData[memoryData])
            PerformanceCsvSave("Frametime-Error.csv", f"Frametime error list", _PerformanceErrorData[frametimeErrorData])
            PerformanceCsvSave("GPUTime-error.csv", f"GPUTime error list", _PerformanceErrorData[gpuTimeErrorData])
            self.ShowMessagebox("Success!")
        
        else:
            self.ShowMessagebox("Failed!")