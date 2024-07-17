from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from Metal_HUD_parse import *
import numpy as np
import time
from GUIStyle import *

_PerformanceCalculationConditions = None
_PerformanceData = None
_PerformanceErrorData  = None

# 스레드
class PerformanceParsingThread(QThread):
    UpdateFileLabelSignal = pyqtSignal(str)
    EmitParsedSignal = pyqtSignal(list, bool, int, int, int, int, str)  # 추가된 신호
    EmitParsedPbarSignal = pyqtSignal(int, int)
    ThreadFinishedSignal = pyqtSignal()

    def __init__(self, FileName, FileData, benchmarkBasedTimeValue, DecimalPoint, parent=None):
        super().__init__(parent)
        self.FileName = FileName
        self.benchmarkBasedTimeValue = benchmarkBasedTimeValue
        self.FileData = FileData
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
        ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, self.DecimalPoint)
        LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, self.DecimalPoint)
        self.emitParsedSignal()
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Done!')
        
        
        # 스레드 종료
        self.ThreadFinishedSignal.emit()
    
    
    def emitParsedSignal(self):
        combined_dict = {**_PerformanceData, **_PerformanceErrorData, **_PerformanceCalculationConditions}

        data = [len(v) for v in combined_dict.values() if isinstance(v, list)]
        row_count = max(data)
        sum_count = sum(data) + len(_PerformanceCalculationConditions.values())
        col_count = len(combined_dict)
        LabelList = list(combined_dict.keys())

        # 메인 스레드에서 스레드 관련 문제 발생시 time.sleep 를 쓰니깐 해결된거 같다.. 뭐지
        sum_pbar = 1
        for col, value in enumerate(combined_dict.values()):
            if isinstance(value, (list, tuple)):
                for row, item in enumerate(value):
                    self.EmitParsedSignal.emit(LabelList, sum_pbar == 1, col_count, row_count, col, row, str(item))
                    self.emitParsedPbarSignal(sum_pbar, sum_count)
                    
                    # 메인 스레드 업데이트 시간
                    if sum_pbar % 3000 == 0:
                        time.sleep(0.05)
                    sum_pbar += 1

            else:
                self.EmitParsedSignal.emit(LabelList, sum_pbar == 1, col_count, row_count, col, 0, str(value))
                self.emitParsedPbarSignal(sum_pbar, sum_count)
                sum_pbar += 1


    def emitParsedPbarSignal(self, sum_pbar, sum_count):
        self.EmitParsedPbarSignal.emit(sum_pbar, sum_count)
    
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