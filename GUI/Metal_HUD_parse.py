import csv
import pandas as pd
from pprint import pprint
import numpy as np


# Metal-HUD.csv 파일 열기
def DataReader(FileName):
    with open(FileName, 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data
    
    # HUDFile = open(FileName, 'r')
    # return csv.reader(HUDFile)

# 데이터 분리
# 콘솔로 들어온 데이터 중 중복된 값이 있어서 제거 처리
# 일부 데이터의 소수점 자리가 <...>로 들어올 때가 있어서 제거 처리
def DataSplit(hudRawData, PerformanceCalculationConditions, PerformanceData, PerformanceErrorData):
    for line in hudRawData:
        if PerformanceCalculationConditions["overlapCheckData"] != line[0]:
                PerformanceCalculationConditions["overlapCheckData"] = line[0]
                PerformanceCalculationConditions["missedFrame"] += int(line[1])
                
                # 메모리 데이터
                PerformanceData['memoryData'].append(np.float64(line[2]))

                for i in range(3, len(line)):
                    if ("<" not in line[i]):
                        if (line[i] != ""):
                            if i % 2 == 1:
                                # 성능 시간 데이터
                                PerformanceData["frameTimeData"].append(np.float64(line[i]))
                                
                            else:
                                # GPU 시간 데이터
                                PerformanceData["gpuTimeData"].append(np.float64(line[i]))
                    else:
                        if i % 2 == 1:
                            PerformanceCalculationConditions["frametimeError"] += 1
                            PerformanceErrorData["frametimeErrorData"].append(line[i])
                        else:
                            PerformanceCalculationConditions["gpuTimeError"] += 1
                            PerformanceErrorData["gpuTimeErrorData"].append(line[i])
        else:
            continue
        

# FPS 계산식
def FPSCalculation(PerformanceCalculationConditions, UnitConversion = 1000, DecimalPoint = 2):
    return np.round(
        (PerformanceCalculationConditions["frameCount"] * 
        PerformanceCalculationConditions["benchmarkBasedTime"] / 
        PerformanceCalculationConditions["secondSum"]) * 
        UnitConversion / 
        PerformanceCalculationConditions["benchmarkBasedTime"],
        DecimalPoint
        )

# FrameTime > FPS 변환
# 평균 FPS = 소수점 3번째 자리에서 반올림 처리 (2자리까지만 표시)
def ConverttoFPS(PerformanceData, PerformanceCalculationConditions, UnitConversion = 1000, DecimalPoint = 2):
    for i in range(len(PerformanceData["frameTimeData"])):
        PerformanceCalculationConditions["secondSum"] += np.float64(PerformanceData["frameTimeData"][i])
        PerformanceCalculationConditions["frameCount"] += 1
        
        if PerformanceCalculationConditions["secondSum"] >= PerformanceCalculationConditions["benchmarkBasedTime"]:
            PerformanceData["FPSData"].append(FPSCalculation(PerformanceCalculationConditions, UnitConversion, DecimalPoint))
            
            # 반복 할때마다 초기화
            PerformanceCalculationConditions["frameCount"] = 0
            PerformanceCalculationConditions["secondSum"] = 0

# 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
# 분모가 0일때 예외처리
def LastDataAvg(PerformanceData, PerformanceCalculationConditions, UnitConversion = 1000, DecimalPoint = 2):
    if PerformanceCalculationConditions["secondSum"] != 0:
        PerformanceData["FPSData"].append(FPSCalculation(PerformanceCalculationConditions, UnitConversion, DecimalPoint))


# 파일 저장 함수
def PerformanceCsvSave(FileName, title, data):
    df = pd.DataFrame({title : data})
    df.to_csv(FileName)


# [benchmarkBasedTime] 여기에 몇 ms마다 FPS 평균을 낼 것인지 입력
# [benchmarkBasedTime] 값이 너무 작으면 실제보다 과하게 프레임이 튀어 보일 수 있음
# [benchmarkBasedTime] 값이 너무 크면 프레임이 튀는 순간을 발견하기 어려움

# 성능 계산 조건식
PerformanceCalculationConditions = {
    "benchmarkBasedTime": 1000,
    "missedFrame": 0,  # 누락된 프레임 갯수
    "frametimeError": 0,  # 소수점 자리가 <...>로 입력된 프레임타임
    "gpuTimeError": 0,  # 소수점 자리가 <...>로 입력된 GPU타임
    "secondSum": 0,
    "frameCount": 0,
    "overlapCheckData": "temp"
}

# 성능 데이터
PerformanceData = {
    "FPSData": [], # 프레임타임을 FPS로 바꾼 것
    "frameTimeData":[], # 프레임타임 데이터 (ms)
    "gpuTimeData":[], # GPU타임 데이터 (ms)
    "memoryData":[] # 메모리 사용량 저장
}

# 성능 오류 데이터
PerformanceErrorData = {
    "frametimeErrorData":[],
    "gpuTimeErrorData":[]
}

if __name__ == "__main__":
    # 성능 데이터 분리
    # DataSplit(DataReader("Metal-HUD.csv"), PerformanceCalculationConditions, PerformanceData, PerformanceErrorData)
    DataSplit(DataReader("output.csv"), PerformanceCalculationConditions, PerformanceData, PerformanceErrorData)

    # FrameTime > FPS 변환
    ConverttoFPS(PerformanceData, PerformanceCalculationConditions, 1000, 2)
    # 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
    LastDataAvg(PerformanceData, PerformanceCalculationConditions, 1000, 2)

    # 파일 저장
    PerformanceCsvSave("FPS-Result.csv", f"FPS - 약 {PerformanceCalculationConditions["benchmarkBasedTime"]} ms마다 평균치 계산", PerformanceData["FPSData"])
    PerformanceCsvSave("Frametime-Result.csv", f"Frametime", PerformanceData["frameTimeData"])
    PerformanceCsvSave("GPUTime-Result.csv", f"GPUTime", PerformanceData["gpuTimeData"])
    PerformanceCsvSave("Memory-Result.csv", f"Memory(MB)", PerformanceData["memoryData"])
    PerformanceCsvSave("Frametime-Error.csv", f"Frametime error list", PerformanceErrorData["frametimeErrorData"])
    PerformanceCsvSave("GPUTime-error.csv", f"GPUTime error list", PerformanceErrorData["gpuTimeErrorData"])

    # pprint(PerformanceData)

    print("\n\nDone! Missed Frame:", PerformanceCalculationConditions["missedFrame"])
    print("Frametime error:", + PerformanceCalculationConditions["frametimeError"])
    print("GPUTime error:", + PerformanceCalculationConditions["gpuTimeError"])