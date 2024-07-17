from PyQt5.QtCore import QThread, pyqtSignal
from Metal_HUD_parse import *
from GUIStyle import *
from collections import OrderedDict

# 초기화
_PerformanceCalculationConditions = None
_PerformanceData = None
_PerformanceErrorData  = None

# 스레드
class PerformanceParsingThread(QThread):
    # 서브 스레드에서 메인 스레드로 데이터를 보낼 신호
    UpdateFileLabelSignal = pyqtSignal(str)
    EmitInitializeTableSignal =  pyqtSignal(list, int, int)
    EmitParsedSignal = pyqtSignal(int, int, str)  # 추가된 신호
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
        try:
            # 파싱 데이터를 저장할 변수 전역변수 설정
            global _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData
            
            # 파싱 데이터를 저장할 변수
            _PerformanceCalculationConditions = PerformanceCalculationConditions()
            _PerformanceData = PerformanceData()
            _PerformanceErrorData = PerformanceErrorData()

            _PerformanceCalculationConditions[benchmarkBasedTime] = self.benchmarkBasedTimeValue
            self.DataParsed()

            # 함수 호출
            self.emitInitializeTableSignal()
            self.emitParsedSignal()
            self.UpdateFileLabelSignal.emit(f'Selected File: "{self.FileName}" Done!')
            
            # 스레드 종료
            self.ThreadFinishedSignal.emit()
        
        except Exception as e:
            pass
        
        finally:
            self.quit()
    
    # 성능 데이터 파싱 함수
    def DataParsed(self):
        self.UpdateFileLabelSignal.emit(f'Selected File: "{self.FileName}" Start...')
        DataSplit(self.FileData, _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData)
        self.UpdateFileLabelSignal.emit(f'Selected File: "{self.FileName}" Loding...')
        ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, self.UnitConversion, self.DecimalPoint)
        self.UpdateFileLabelSignal.emit(f'Selected File: "{self.FileName}" Loding(Saveable.)...')
    
    # 여러개의 딕셔너리를 하나의 딕셔너리로 만듦
    def CombinedDict(self):
        combined_dict = OrderedDict()
        combined_dict.update(_PerformanceData)
        combined_dict.update(_PerformanceErrorData)
        combined_dict.update(_PerformanceCalculationConditions)
        return combined_dict
    
    # 컴빈드 데이터 계산
    def CombinedDictData(self, combined_dict):
        return [len(v) for v in combined_dict.values() if isinstance(v, list)]
    
    # 테이블에 row, col 초기 설정 데이터를 전달하는 함수
    def emitInitializeTableSignal(self):
        combined_dict = self.CombinedDict()
        data = self.CombinedDictData(combined_dict)
        label_list = list(combined_dict.keys())
        col_count = len(combined_dict)
        row_count = max(data) # Key 값 중에 가장 많은 Value 하나 찾음.
        self.EmitInitializeTableSignal.emit(label_list, col_count, row_count)
        
    
    # 파싱 데이터를 테이블에 데이터를 전달하는 함수
    def emitParsedSignal(self):
        combined_dict = self.CombinedDict()
        data = self.CombinedDictData(combined_dict)
        sum_count = sum(data) + len(_PerformanceCalculationConditions.values()) # 프로그래스바 100% 기준 해당하는 값

        sum_pbar = 1
        for col, value in enumerate(combined_dict.values()):
            # 타입 검사
            if isinstance(value, (list, tuple)):
                for row, item in enumerate(value):
                    self.emitParsedSignalItem(col, row, str(item))
                    self.emitParsedPbarValue(sum_pbar, sum_count)
                    self.overhead(sum_pbar)
                    sum_pbar += 1

            # 데이터 배열이 아닐때
            else:
                self.emitParsedSignalItem(col, 0, str(value))
                self.emitParsedPbarValue(sum_pbar, sum_count)
                self.overhead(sum_pbar)
                sum_pbar += 1
    
    
    # 테이블 아이템 신호 업데이트
    def emitParsedSignalItem(self, col, row, item):
        self.EmitParsedSignal.emit(col, row, item)
    
    # 진행상황 프로그래스바 신호 업데이트
    def emitParsedPbarValue(self, sum_pbar, sum_count):
        self.EmitParsedPbarSignal.emit(sum_pbar, sum_count)

    # 메인 스레드가 업데이트를 하기위해 서브 스레드를 잠시 멈추는 함수
    def overhead(self, sum_pbar):
        if sum_pbar % 3000 == 0:
            self.msleep(100)


# 파일로 저장
class PerformanceParsingResultsSaveThread(QThread):
    MsgBoxNotifications = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
    
    def run(self):
        try:
            if all([_PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData]):
                PerformanceCsvSave("FPS-Result.csv", f"FPS - 약 {_PerformanceCalculationConditions[benchmarkBasedTime]} ms마다 평균치 계산", _PerformanceData[FPSData])
                PerformanceCsvSave("Frametime-Result.csv", f"Frametime", _PerformanceData[frameTimeData])
                PerformanceCsvSave("GPUTime-Result.csv", f"GPUTime", _PerformanceData[gpuTimeData])
                PerformanceCsvSave("Memory-Result.csv", f"Memory(MB)", _PerformanceData[memoryData])
                PerformanceCsvSave("Frametime-Error.csv", f"Frametime error list", _PerformanceErrorData[frametimeErrorData])
                PerformanceCsvSave("GPUTime-error.csv", f"GPUTime error list", _PerformanceErrorData[gpuTimeErrorData])
                self.MsgBoxNotifications.emit("Success!")
                
            else:
                self.MsgBoxNotifications.emit("Failed!")
                
        except Exception as e:
            self.MsgBoxNotifications.emit(f"Error: {str(e)}")
            
        finally:
            self.quit()