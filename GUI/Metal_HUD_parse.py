import csv
import pandas as pd
# from pprint import pprint
from config_paths import *
from config_paths_Utils import *
from applog import *
import os

logger = InitLogger(CurrentFileName(__file__))


# Metal-HUD.csv 파일 열기
def DataReader(FileName):
    try:
        if FileName.endswith(".csv"):
            with open(FileName, 'r', newline='') as f:
                reader = csv.reader(f)
                data = list(reader)
            return data
        
        else:
            logger.debug("DataReader File Extension Selection Error: Not a *.csv file.")
            return None
    
    except Exception as e:
        logger.error(f"데이터를 불러오는 과정에 문제가 생겼습니다. | Error Code: {e}")
        return None

# 데이터 분리
def DataSplit(hudRawData, PerformanceCalculationConditions, PerformanceData, PerformanceErrorData, DecimalPoint = 2):
    try:
        
        # 소수점 값 처리 조건문
        # a. 2 보다 값이 크면 2 를 반환
        # b. 2 보다 값이 작으면 임의 값을 반환
        DecimalPointValue = DecimalPoint if DecimalPoint <= 2 else 2
        
        for line in hudRawData:
            # 콘솔로 들어온 데이터 중 중복된 값이 있어서 제거 처리
            if PerformanceCalculationConditions[overlapCheckData] != line[0]:
                    PerformanceCalculationConditions[overlapCheckData] = line[0]
                    PerformanceCalculationConditions[missedFrame] = float(line[1])
                    
                    # 메모리 데이터
                    PerformanceData[memoryData].append(round(float(line[2]), DecimalPointValue))

                    for i in range(3, len(line)):
                        # 일부 데이터의 소수점 자리가 <...>로 들어올 때가 있어서 제거 처리
                        if ("<" not in line[i]):
                            if (line[i] != ""):
                                if i % 2 == 1:
                                    # 성능 시간 데이터
                                    PerformanceData[frameTimeData].append(round(float(line[i]), DecimalPointValue))
                                    
                                else:
                                    # GPU 시간 데이터
                                    PerformanceData[gpuTimeData].append(round(float(line[i]), DecimalPointValue))
                        else:
                            if i % 2 == 1:
                                PerformanceCalculationConditions[frametimeError] += 1
                                PerformanceErrorData[frametimeErrorData].append(line[i])
                            else:
                                PerformanceCalculationConditions[gpuTimeError] += 1
                                PerformanceErrorData[gpuTimeErrorData].append(line[i])
            else:
                continue
            
    except Exception as e:
        logger.error(f"데이터를 분리하는 과정에 문제가 생겼습니다. | Error Code: {e}")
        return None

# FPS 계산식
def FPSCalculation(PerformanceCalculationConditions, DecimalPoint = 2):
    try:
        return round(
        (PerformanceCalculationConditions[frameCount] * 
        PerformanceCalculationConditions[benchmarkBasedTime] / 
        PerformanceCalculationConditions[secondSum]) * 
        1000 / 
        PerformanceCalculationConditions[benchmarkBasedTime],
        DecimalPoint
        )
        
    except Exception as e:
        logger.error(f"FPS 계산식에 문제가 생겼습니다. | Error Code: {e}")
        return None
        
# FrameTime > FPS 변환
# 평균 FPS = 소수점 3번째 자리에서 반올림 처리 (2자리까지만 표시)
def ConverttoFPS(PerformanceData, PerformanceCalculationConditions, DecimalPoint = 2):
    # 자투리 시간 오차를 줄이기 위해 추가. 이게 없으면 1초당 약 1/FPS 만큼의 오차가 생김
    overTempFrameTimeSum = 0.0
    try:
        for i in range(len(PerformanceData[frameTimeData])):
            PerformanceCalculationConditions[secondSum] += float(PerformanceData[frameTimeData][i])
            PerformanceCalculationConditions[frameCount] += 1
            
            if PerformanceCalculationConditions[secondSum] >= PerformanceCalculationConditions[benchmarkBasedTime] - overTempFrameTimeSum:
                PerformanceData[FPSData].append(FPSCalculation(PerformanceCalculationConditions, DecimalPoint))
                
                # 반복 할때마다 초기화
                overTempFrameTimeSum = PerformanceCalculationConditions[secondSum] - (1000 - overTempFrameTimeSum)
                PerformanceCalculationConditions[frameCount] = 0
                PerformanceCalculationConditions[secondSum] = 0
                
    except Exception as e:
        logger.error(f"FPS를 변환하는 과정에 문제가 생겼습니다. | Error Code: {e}")
        return None

# 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
def LastDataAvg(PerformanceData, PerformanceCalculationConditions, DecimalPoint = 2):
    try:
        # 분모가 0일때 예외처리
        if PerformanceCalculationConditions[secondSum] != 0:
            PerformanceData[FPSData].append(FPSCalculation(PerformanceCalculationConditions, DecimalPoint))
    except Exception as e:
        logger.error(f"마지막 FPS 데이터를 변환하는 과정에 문제가 생겼습니다. | Error Code: {e}")

# 파일 저장 함수
def PerformanceCsvSave(ParseDataSavePath, FileName, title, data, Index_number):
    try:
        df = pd.DataFrame({title : data})
        df.to_csv(os.path.join(ParseDataSavePath, FileName), index=Index_number)
        
    except Exception as e:
        logger.error(f"결과값을 저장하는 과정에 문제가 생겼습니다. | Error Code: {e}")

#benchmarkBasedTime 여기에 몇 ms마다 FPS 평균을 낼 것인지 입력
#benchmarkBasedTime 값이 너무 작으면 실제보다 과하게 프레임이 튀어 보일 수 있음
#benchmarkBasedTime 값이 너무 크면 프레임이 튀는 순간을 발견하기 어려움

# 성능 계산 조건식
def PerformanceCalculationConditions():
    return {
        benchmarkBasedTime: 1000,
        missedFrame: 0.0,  # 누락된 프레임 갯수
        frametimeError: 0,  # 소수점 자리가 <...>로 입력된 프레임타임
        gpuTimeError: 0,  # 소수점 자리가 <...>로 입력된 GPU타임
        secondSum: 0,
        frameCount: 0,
        overlapCheckData: "temp"
    }

# 성능 데이터
def PerformanceData():
    return {
        FPSData: [], # 프레임타임을 FPS로 바꾼 것
        frameTimeData:[], # 프레임타임 데이터 (ms)
        gpuTimeData:[], # GPU타임 데이터 (ms)
        memoryData:[] # 메모리 사용량 저장
    }

# 성능 오류 데이터
def PerformanceErrorData():
    return {
        frametimeErrorData:[],
        gpuTimeErrorData:[]
    }

if __name__ == "__main__":
    # 딕셔너리 초기화
    _PerformanceCalculationConditions = PerformanceCalculationConditions()
    _PerformanceData = PerformanceData()
    _PerformanceErrorData = PerformanceErrorData()

    # 소수점 반올림
    DecimalPoint = 2
    
    # Parse 데이터 저장시 인덱스 번호 표시 여부
    include_index = False
    
    # 성능 데이터 분리
    DataSplit(DataReader("output3.csv"), _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData, DecimalPoint)

    # FrameTime > FPS 변환
    ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, DecimalPoint)
    # 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
    LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, DecimalPoint)

    # 파일 저장
    # Parse Data Save FilePath
    ParseDataSavePath = MakeFolder(f"Parse_Save/{CurrentTime()}")
    
    
    # 저장할 파일 이름과 관련된 정보
    performance_data = {
        "FPS-Result.csv": (f"FPS - 약 {_PerformanceCalculationConditions[benchmarkBasedTime]} ms마다 평균치 계산", _PerformanceData[FPSData]),
        "Frametime-Result.csv": (f"Frametime", _PerformanceData[frameTimeData]),
        "GPUTime-Result.csv": (f"GPUTime", _PerformanceData[gpuTimeData]),
        "Memory-Result.csv": (f"Memory(MB)", _PerformanceData[memoryData]),
        "Frametime-Error.csv": (f"Frametime error list", _PerformanceErrorData[frametimeErrorData]),
        "GPUTime-error.csv": (f"GPUTime error list", _PerformanceErrorData[gpuTimeErrorData]),
    }

    # 반복문을 통해 파일 저장
    for filename, (description, data) in performance_data.items():
        PerformanceCsvSave(ParseDataSavePath, filename, description, data, include_index)
    
    
    logger.debug(f"Done! Missed Frame: {_PerformanceCalculationConditions[missedFrame]}")
    logger.debug(f"Frametime error: {_PerformanceCalculationConditions[frametimeError]}")
    logger.debug(f"GPUTime error: {_PerformanceCalculationConditions[gpuTimeError]}")