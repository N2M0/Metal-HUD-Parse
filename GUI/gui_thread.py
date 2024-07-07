from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QApplication
from Metal_HUD_parse import *
import numpy as np
from gui_style import *

_PerformanceCalculationConditions = None
_PerformanceData = None
_PerformanceErrorData  = None
# app = QApplication(sys.argv)

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
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Done!')
        
        # pprint(_PerformanceData)
        pprint(np.mean(_PerformanceData[FPSData]))
        
        # 스레드 종료
        self.ThreadFinishedSignal.emit()


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