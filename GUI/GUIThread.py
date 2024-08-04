from PyQt5.QtCore import QThread, pyqtSignal
from Metal_HUD_parse import *
from GUIStyle import *
from collections import OrderedDict
import sys
from Json_Utils import *
from config_paths import *
from applog import *
import numpy as np


logger = InitLogger(CurrentFileName(__file__))

# 초기화
_PerformanceCalculationConditions = None
_PerformanceData = None
_PerformanceErrorData  = None

# 통계 계산 실행 조건 함수.
def Statistical_Function_Manager(func, values):
    if len(values) == 0:
        return None  # 빈 리스트에 대한 처리
    return func(values)

# 스레드
class PerformanceParsingThread(QThread):
    # 서브 스레드에서 메인 스레드로 데이터를 보낼 신호
    ParseStartBtnState = pyqtSignal(bool)
    UpdateFileLabelSignal = pyqtSignal(str)
    EmitTableState = pyqtSignal(bool, object)
    EmitPbarState = pyqtSignal(bool, object)
    EmitInitializeTableSignal =  pyqtSignal(list, list, int, int)
    EmitParsedSignal = pyqtSignal(int, int, str)
    EmitParsedPbarSignal = pyqtSignal(int, int)
    EmitTableResize = pyqtSignal()
    ThreadFinishedSignal = pyqtSignal()
    
    def __init__(self, parent, FileName, benchmarkBasedTimeValue, DecimalPoint):
        super().__init__(parent)
        
        self.FileName = FileName
        self.benchmarkBasedTimeValue = benchmarkBasedTimeValue
        self.DecimalPoint = DecimalPoint
        
        self.parent = parent
        self.ParsedResultsTable = self.parent.ParsedResultsTable
        self.ParsedPbar = self.parent.ParsedPbar
        
    # 성능 파싱 시작
    def run(self):
        try:
            # 파싱 데이터를 저장할 변수 전역변수 설정
            global _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData
            
            
            # 설정 값 가져오기
            self.settings = OpenJson(SetDataFilePath)

            # 파싱이 시작중에는 버튼 비활성화
            self.ParseStartBtnState.emit(False)
            
            # 파싱 데이터를 저장할 변수
            _PerformanceCalculationConditions = PerformanceCalculationConditions()
            _PerformanceData = PerformanceData()
            _PerformanceErrorData = PerformanceErrorData()

            _PerformanceCalculationConditions[benchmarkBasedTime] = self.benchmarkBasedTimeValue
            # 데이터 파싱 계산.
            self.DataParsed()
            # 불필요한 키-값 제거
            self.RemoveKeys()

            # 미리보기 테이블 사용 여부
            Preview_data_used_change = True if self.settings[Preview_data] == Preview_data_parmeters[Preview_data_default] else False
            
            # 미리보기 테이블 보기 모드
            Preview_data_viewing_mode_change = True if self.settings[Preview_data_viewing_mode] == Preview_data_viewing_mode_parmeters[Preview_data_viewing_mode_default] else False
            
            self.EmitTableState.emit(Preview_data_used_change, self.ParsedResultsTable)
            self.EmitPbarState.emit(Preview_data_used_change, self.ParsedPbar)
            
            # 필요 함수 호출.
            self.emitInitializeTableSignal(Preview_data_used_change, Preview_data_viewing_mode_change)
            self.emitParsedSignal(Preview_data_used_change, Preview_data_viewing_mode_change)
            
            # 완료 레이블 시그널.
            self.UpdateFileLabelSignal.emit(f'Selected File: "{self.FileName}" Done!')
            
            # 테이블 리사이즈
            self.EmitTableResize.emit()
            
        
        except Exception as e:
            logger.error(f"성능 파싱 스레드에서 실행 내용을 정의하는 데에 문제가 생겼습니다. | Error Code: {e}")
            
            # 오류 발생시 바로 종료.
            sys.exit(1)
        
        finally:
            # 스레드 종료시 파싱 버튼을 활성화
            self.ParseStartBtnState.emit(True)
            
            # 스레드 종료
            self.ThreadFinishedSignal.emit()

            
    # 성능 데이터 파싱 함수
    def DataParsed(self):
        try:
            self.FileData = DataReader(self.FileName)
            self.UpdateFileLabelSignal.emit(f'Selected File: "{self.FileName}" Start...')
            DataSplit(self.FileData, _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData, self.DecimalPoint)
            self.UpdateFileLabelSignal.emit(f'Selected File: "{self.FileName}" Loding...')
            ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, self.DecimalPoint)
            LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, self.DecimalPoint)
            self.UpdateFileLabelSignal.emit(f'Selected File: "{self.FileName}" Loding(Saveable.)...')
            
        except Exception as e:
            logger.error(f"스레드에서 데이터 Parse 함수를 실행하는 중에 문제가 생겼습니다. | Error Code: {e}")
            return None
    
    
    def RemoveKeys(self):
        try:
            # 필요없는 키-값 제거
            remove_keys = [secondSum, frameCount, overlapCheckData]
            for key in remove_keys:
                _PerformanceCalculationConditions.pop(key)
                
        except Exception as e:
            logger.error(f"불필요한 Keys:Values를 제거하는데 문제가 생겼습니다. | Error Code: {e}")
            return None
        
    # 여러개의 딕셔너리를 하나의 딕셔너리로 만듦
    def CombinedDict(self):
        try:
            # 딕셔너리 합치기
            combined_dict = OrderedDict()
            combined_dict.update(_PerformanceData)
            combined_dict.update(_PerformanceErrorData)
            combined_dict.update(_PerformanceCalculationConditions)
            
            return combined_dict
        
        except Exception as e:
            logger.error(f"여러개의 딕셔너리를 합치는 중에 문제가 생겼습니다. | Error Code: {e}")
            return None
    
    # 컴빈드 데이터 계산
    def CombinedDictDataCalculate(self, combined_dict):
        try:
            return [len(v) for v in combined_dict.values() if isinstance(v, list)]
        except Exception as e:
            logger.error(f"합쳐진 딕셔너리 데이터를 계산하는데 문제가 생겼습니다. | Error Code: {e}")
            return None
        
    # 테이블에 row, col 초기 설정 데이터를 전달하는 함수
    def emitInitializeTableSignal(self, used, state):
        if used:
            try:
                combined_dict = self.CombinedDict()
                data = self.CombinedDictDataCalculate(combined_dict)
                x_label_list = list(combined_dict.keys())
                col_count = len(combined_dict)
                
                # 원시 모드
                if state:
                    row_count = max(data) # Key 값 중에 가장 많은 Value 하나 찾음.
                    self.EmitInitializeTableSignal.emit(x_label_list, [], col_count, row_count)
                
                # 통계 모드
                else:
                    # 통계 함수
                    self.statistical_functions = {
                        "Maximum":np.max,
                        "Average": np.mean,
                        "Median": np.median,
                        "Minimum": np.min,
                        "Variance": np.var,
                        "Stdev": np.std,
                    }
                    
                    y_label_list = list(self.statistical_functions.keys())
                    row_count = len(y_label_list)
                    self.EmitInitializeTableSignal.emit(x_label_list, y_label_list, col_count, row_count)

            except Exception as e:
                logger.error(f"미리보기 테이블에 초기값을 방출하는데 문제가 생겼습니다. | Error Code: {e}")
                return None
    
    # 파싱 데이터를 테이블하고 프로그래스바에 데이터를 전달하는 함수
    def emitParsedSignal(self, used, viewing_mode):
        if used:
            try:
                # 원시 데이터                                  # 통계 데이터
                self.rawDataProcessing() if viewing_mode else self.statisticalDataProcessing()
                
            except Exception as e:
                logger.error(f"미리보기 테이블 시그널, 프로그래스바 시그널에 데이터를 전달하는 과정에 문제가 생겼습니다. | Error Code: {e}")
                return None
    
    # 원시 데이터
    def rawDataProcessing(self):
        combined_dict = self.CombinedDict()
        data = self.CombinedDictDataCalculate(combined_dict)
        sum_count = sum(data) + len(_PerformanceCalculationConditions.values()) # 프로그래스바 100% 기준 해당하는 값
        
        # 프로그래스바 계산 초기값
        sum_pbar = 1
        for col, value in enumerate(combined_dict.values()):
            # 타입 검사
            if isinstance(value, (list, tuple)):
                for row, item in enumerate(value):
                    if self.isInterruptionRequested():
                        logger.info("파싱 스레드가 중단 요청을 받았습니다.")
                        return
                    
                    self.emitParsedSignalItem(col, row, str(item))
                    self.emitParsedPbarValue(sum_pbar, sum_count)
                    self.overhead(sum_pbar)
                    sum_pbar += 1

            # 데이터 배열이 아닐때
            else:
                if self.isInterruptionRequested():
                    logger.info("파싱 스레드가 중단 요청을 받았습니다.")
                    return
                
                self.emitParsedSignalItem(col, 0, str(value))
                self.emitParsedPbarValue(sum_pbar, sum_count)
                self.overhead(sum_pbar)
                sum_pbar += 1
                
    
    # 통계화된 데이터
    def statisticalDataProcessing(self):
        combined_dict = self.CombinedDict()
        repeat_value = list(self.statistical_functions.values())
        sum_count = len(combined_dict.keys()) * len(repeat_value) # 프로그래스바 100% 기준 해당하는 값
        
        # 프로그래스바 계산 초기값
        sum_pbar = 1
        for col, value in enumerate(combined_dict.values()):
            if self.isInterruptionRequested():
                logger.info("파싱 스레드가 중단 요청을 받았습니다.")
                return
            
            for row, func in enumerate(repeat_value):
                if self.isInterruptionRequested():
                    logger.info("파싱 스레드가 중단 요청을 받았습니다.")
                    return
                
                # 타입 검사
                if isinstance(value, (list, tuple)):
                    # 내부 값들이 모두 int 또는 float인지 확인
                    value_type = Statistical_Function_Manager(func, value) if all(isinstance(v, (int, float)) for v in value) else value
                    
                    # 값이 int 또는 float일 경우에만 추가
                    Selecting_value = str(round(value_type, self.DecimalPoint)) if isinstance(value_type, (int, float)) else str(f"Errors: {len(value_type) if value_type is not None else None} counted")
                    self.emitParsedSignalItem(col, row, Selecting_value)
                    
                else:
                    self.emitParsedSignalItem(col, row, str(round(value, self.DecimalPoint)))
                
                # 프로그래스바 및 성능 모드 계산.
                self.emitParsedPbarValue(sum_pbar, sum_count)
                self.overhead(sum_pbar)
                sum_pbar += 1

    
    # 테이블 아이템 신호 업데이트
    def emitParsedSignalItem(self, col, row, item):
        try:
            self.EmitParsedSignal.emit(col, row, item)

        except Exception as e:
            logger.error(f"미리보기 테이블에 데이터를 방출하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            return None
    
    # 진행상황 프로그래스바 신호 업데이트
    def emitParsedPbarValue(self, sum_pbar, sum_count):
        try:
            self.EmitParsedPbarSignal.emit(sum_pbar, sum_count)

        except Exception as e:
            logger.error(f"프로그래스바에 데이터를 방출하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            return None
            
    # 메인 스레드가 업데이트를 하기위해 서브 스레드를 잠시 멈추는 함수
    # 성능 제한 모드, 성능 우선 모드 두가지 모드로 제공할 것.
    def overhead(self, sum_pbar):
        try:
            if self.settings[Startup_mode] == Startup_mode_parmeters[Startup_mode_default]:
                if sum_pbar % 3000 == 0:
                    self.msleep(100)

        except Exception as e:
            logger.error(f"성능 제한 모드에 문제가 생겼습니다. | Error Code: {e}")
            return None


# 파일로 저장
class PerformanceParsingResultsSaveThread(QThread):
    ParsedSaveBtnState = pyqtSignal(bool)
    MsgBoxNotifications = pyqtSignal(str)
    ThreadFinishedSignal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def run(self):
        try:
            # 스레드 시작시 파일 저장 버튼을 비활성화
            self.ParsedSaveBtnState.emit(False)
            self.Saved()
                
        except Exception as e:
            logger.error(f"데이터 저장 스레드에서 실행 내용을 정의하는 데에 문제가 생겼습니다. | Error Code: {e}")
            self.MsgBoxNotifications.emit(f"Error Code: {str(e)}")
            
        finally:
            # 스레드 종료시 파일 저장 버튼을 활성화
            self.ParsedSaveBtnState.emit(True)
            
            # if self.isInterruptionRequested():
            #     logger.info("데이터 저장 스레드가 중단 요청을 받았습니다.")
            #     return
            
            # 스레드 종료
            self.ThreadFinishedSignal.emit()
            
    
    def Saved(self):
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