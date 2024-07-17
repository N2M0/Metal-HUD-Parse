import csv
import pandas as pd
from pprint import pprint
from constant import *

# Metal-HUD.csv 파일 열기
def DataReader(FileName):
    with open(FileName, 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data
    
    # HUDFile = open(FileName, 'r')
    # return csv.reader(HUDFile)

# 데이터 분리
def DataSplit(hudRawData, PerformanceCalculationConditions, PerformanceData, PerformanceErrorData):
    for line in hudRawData:
        # 콘솔로 들어온 데이터 중 중복된 값이 있어서 제거 처리
        if PerformanceCalculationConditions[overlapCheckData] != line[0]:
                PerformanceCalculationConditions[overlapCheckData] = line[0]
                PerformanceCalculationConditions[missedFrame] += int(line[1])
                
                # 메모리 데이터
                PerformanceData[memoryData].append(float(line[2]))

                for i in range(3, len(line)):
                    # 일부 데이터의 소수점 자리가 <...>로 들어올 때가 있어서 제거 처리
                    if ("<" not in line[i]):
                        if (line[i] != ""):
                            if i % 2 == 1:
                                # 성능 시간 데이터
                                PerformanceData[frameTimeData].append(float(line[i]))
                                
                            else:
                                # GPU 시간 데이터
                                PerformanceData[gpuTimeData].append(float(line[i]))
                    else:
                        if i % 2 == 1:
                            PerformanceCalculationConditions[frametimeError] += 1
                            PerformanceErrorData[frametimeErrorData].append(line[i])
                        else:
                            PerformanceCalculationConditions[gpuTimeError] += 1
                            PerformanceErrorData[gpuTimeErrorData].append(line[i])
        else:
            continue
        

# FPS 계산식
def FPSCalculation(PerformanceCalculationConditions, UnitConversion = 1000, DecimalPoint = 2):
    return round(
        (PerformanceCalculationConditions[frameCount] * 
        PerformanceCalculationConditions[benchmarkBasedTime] / 
        PerformanceCalculationConditions[secondSum]) * 
        UnitConversion / 
        PerformanceCalculationConditions[benchmarkBasedTime],
        DecimalPoint
        )

# FrameTime > FPS 변환
# 평균 FPS = 소수점 3번째 자리에서 반올림 처리 (2자리까지만 표시)
def ConverttoFPS(PerformanceData, PerformanceCalculationConditions, UnitConversion = 1000, DecimalPoint = 2):
    for i in range(len(PerformanceData[frameTimeData])):
        PerformanceCalculationConditions[secondSum] += float(PerformanceData[frameTimeData][i])
        PerformanceCalculationConditions[frameCount] += 1
        
        if PerformanceCalculationConditions[secondSum] >= PerformanceCalculationConditions[benchmarkBasedTime]:
            PerformanceData[FPSData].append(FPSCalculation(PerformanceCalculationConditions, UnitConversion, DecimalPoint))
            
            # 반복 할때마다 초기화
            PerformanceCalculationConditions[frameCount] = 0
            PerformanceCalculationConditions[secondSum] = 0

# 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
def LastDataAvg(PerformanceData, PerformanceCalculationConditions, UnitConversion = 1000, DecimalPoint = 2):
    # 분모가 0일때 예외처리
    if PerformanceCalculationConditions[secondSum] != 0:
        PerformanceData[FPSData].append(FPSCalculation(PerformanceCalculationConditions, UnitConversion, DecimalPoint))


# 파일 저장 함수
def PerformanceCsvSave(FileName, title, data):
    df = pd.DataFrame({title : data})
    df.to_csv(FileName)


#benchmarkBasedTime 여기에 몇 ms마다 FPS 평균을 낼 것인지 입력
#benchmarkBasedTime 값이 너무 작으면 실제보다 과하게 프레임이 튀어 보일 수 있음
#benchmarkBasedTime 값이 너무 크면 프레임이 튀는 순간을 발견하기 어려움

# 성능 계산 조건식
def PerformanceCalculationConditions():
    return {
        benchmarkBasedTime: 1000,
        missedFrame: 0,  # 누락된 프레임 갯수
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

    # 성능 데이터 분리
    DataSplit(DataReader("output.csv"), _PerformanceCalculationConditions, _PerformanceData, _PerformanceErrorData)

    # FrameTime > FPS 변환
    ConverttoFPS(_PerformanceData, _PerformanceCalculationConditions, 1000, 2)
    # 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
    LastDataAvg(_PerformanceData, _PerformanceCalculationConditions, 1000, 2)

    # 파일 저장
    # 딕셔너리 key를 정의된 key 변수로 교체 권장
    # PerformanceCsvSave("FPS-Result.csv", f"FPS - 약 {_PerformanceCalculationConditions['benchmarkBasedTime']} ms마다 평균치 계산", PerformanceData["FPSData"])
    # PerformanceCsvSave("Frametime-Result.csv", f"Frametime", _PerformanceData["frameTimeData"])
    # PerformanceCsvSave("GPUTime-Result.csv", f"GPUTime", _PerformanceData["gpuTimeData"])
    # PerformanceCsvSave("Memory-Result.csv", f"Memory(MB)", _PerformanceData["memoryData"])
    # PerformanceCsvSave("Frametime-Error.csv", f"Frametime error list", _PerformanceErrorData["frametimeErrorData"])
    # PerformanceCsvSave("GPUTime-error.csv", f"GPUTime error list", _PerformanceErrorData["gpuTimeErrorData"])

    # pprint(_PerformanceData)

    # print("\n\nDone! Missed Frame:", _PerformanceCalculationConditions["missedFrame"])
    # print("Frametime error:", _PerformanceCalculationConditions["frametimeError"])
    # print("GPUTime error:", _PerformanceCalculationConditions["gpuTimeError"])
    
    for key, value in _PerformanceData.items():
        for value in value:
            print(value)