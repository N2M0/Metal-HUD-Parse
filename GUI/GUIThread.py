from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from Metal_HUD_parse import *
from GUIStyle import *

# 초기화
_PerformanceCalculationConditions = None
_PerformanceData = None
_PerformanceErrorData  = None

# 스레드
class PerformanceParsingThread(QThread):
    # 서브 스레드에서 메인 스레드로 데이터를 보낼 신호
    UpdateFileLabelSignal = pyqtSignal(str)
    EmitParsedSignal = pyqtSignal(list, bool, int, int, int, int, str)  # 추가된 신호
    EmitParsedPbarSignal = pyqtSignal(int, int)
    ThreadFinishedSignal = pyqtSignal()

    def __init__(self, parent, FileName, FileData, benchmarkBasedTimeValue, UnitConversion, DecimalPoint):
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
        # 파싱 데이터를 저장할 변수 전역변수 설정
        global _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData
        
        # 파싱 데이터를 저장할 변수
        _PerformanceCalculationConditions = PerformanceCalculationConditions()
        _PerformanceData = PerformanceData()
        _PerformanceErrorData = PerformanceErrorData()

        _PerformanceCalculationConditions[benchmarkBasedTime] = self.benchmarkBasedTimeValue
        
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Start...')
        DataSplit(self.FileData, _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Loding...')
        ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Loding(Saveable.)...')

        # 함수 호출
        self.emitParsedSignal()
        self.UpdateFileLabelSignal.emit(f'Selected File: {self.FileName} Done!')
        
        
        # 스레드 종료
        self.ThreadFinishedSignal.emit()
    
    # 파싱 데이터를 테이블에 데이터를 전달하는 함수
    def emitParsedSignal(self):
        combined_dict = {**_PerformanceData, **_PerformanceErrorData, **_PerformanceCalculationConditions}

        data = [len(v) for v in combined_dict.values() if isinstance(v, list)]
        row_count = max(data) # Key 값 중에 가장 많은 Value 하나 찾음.
        sum_count = sum(data) + len(_PerformanceCalculationConditions.values()) # 프로그래스바 100% 기준 해당하는 값
        col_count = len(combined_dict)
        LabelList = list(combined_dict.keys())

        sum_pbar = 1
        for col, value in enumerate(combined_dict.values()):
            # 타입 검사
            if isinstance(value, (list, tuple)):
                for row, item in enumerate(value):
                    self.EmitParsedSignal.emit(LabelList, sum_pbar == 1, col_count, row_count, col, row, str(item))
                    self.emitParsedPbarSignal(sum_pbar, sum_count)
                    self.overhead(sum_pbar)
                    sum_pbar += 1

            # 데이터 배열이 아닐때
            else:
                self.EmitParsedSignal.emit(LabelList, sum_pbar == 1, col_count, row_count, col, 0, str(value))
                self.emitParsedPbarSignal(sum_pbar, sum_count)
                self.overhead(sum_pbar)
                sum_pbar += 1
    
    # 진행상황 프로그래스바 신호 업데이트
    def emitParsedPbarSignal(self, sum_pbar, sum_count):
        self.EmitParsedPbarSignal.emit(sum_pbar, sum_count)

    # 메인 스레드가 업데이트를 하기위해 서브 스레드를 잠시 멈추는 함수
    def overhead(self, sum_pbar):
        if sum_pbar % 3000 == 0:
            self.msleep(30)
    
# 파일로 저장
class PerformanceParsingResultsSaveThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
    
    # 메시지박스
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