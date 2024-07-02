import csv
import pandas as pd

# Metal-HUD.csv 파일 열기
HUDFile = open('Metal-HUD.csv','r')

#여기에 몇 ms마다 FPS 평균을 낼 것인지 입력
#값이 너무 작으면 실제보다 과하게 프레임이 튀어 보일 수 있음
#값이 너무 크면 프레임이 튀는 순간을 발견하기 어려움
benchmarkBasedTime = 1000

hudRawData = csv.reader(HUDFile)
missedFrame = 0  # 누락된 프레임 갯수
frametimeError = 0 # 소수점 자리가 <...>로 입력된 프레임타임
gpuTimeError = 0 # 소수점 자리가 <...>로 입력된 GPU타임

FPSData = []  # 프레임타임을 FPS로 바꾼 것
frameTimeData = []  # 프레임타임 데이터 (ms)
gpuTimeData = []  # GPU타임 데이터 (ms)
memoryData = []  # 메모리 사용량 저장

frametimeErrorData = []
gpuTimeErrorData = []

secondSum = 0
frameCount = 0

overlapCheckData = "temp"

# 데이터 분리
# 콘솔로 들어온 데이터 중 중복된 값이 있어서 제거 처리
# 일부 데이터의 소수점 자리가 <...>로 들어올 때가 있어서 제거 처리
for line in hudRawData:
    if overlapCheckData != line[0]:
            overlapCheckData = line[0]
            missedFrame += int(line[1])
            memoryData.append(line[2])

            for i in range(3, len(line)):
                if ("<" not in line[i]):
                    if (line[i] != ""):
                        if i % 2 == 1:
                            frameTimeData.append(float(line[i]))
                        else:
                            gpuTimeData.append(float(line[i]))
                else:
                    if i % 2 == 1:
                        frametimeError += 1
                        frametimeErrorData.append(line[i])
                    else:
                        gpuTimeError += 1
                        gpuTimeErrorData.append(line[i])
    else:
        continue

HUDFile.close()
# 데이터 분리 끝

# FrameTime > FPS 변환
# 평균 FPS = 소수점 3번째 자리에서 반올림 처리 (2자리까지만 표시)
for i in range(len(frameTimeData)):
    secondSum += float(frameTimeData[i])
    frameCount += 1
    if secondSum >= benchmarkBasedTime:
        FPSData.append(round((frameCount * benchmarkBasedTime / secondSum) * 1000 / benchmarkBasedTime, 2))
        frameCount = 0
        secondSum = 0

# 마지막에 남은 1초 안되는 자투리 데이터로 평균 FPS 계산
# 분모가 0일때 예외처리
if secondSum != 0:
    FPSData.append(round((frameCount * benchmarkBasedTime / secondSum) * 1000 / benchmarkBasedTime, 2))

# 파일로 저장
FPSDataFrame = pd.DataFrame({'FPS - 약 ' + str(benchmarkBasedTime) + "ms마다 평균치 계산" : FPSData})
FPSDataFrame.to_csv('FPS-Result.csv')

frametimeDataFrame = pd.DataFrame({'Frametime' : frameTimeData})
frametimeDataFrame.to_csv('Frametime-Result.csv')

gpuTimeDataFrame = pd.DataFrame({'GPUTime' : gpuTimeData})
gpuTimeDataFrame.to_csv('GPUTime-Result.csv')

memoryDataFrame = pd.DataFrame({'Memory(MB)' : memoryData})
memoryDataFrame.to_csv('Memory-Result.csv')

frametimeErrorDataFrame = pd.DataFrame({'Frametime error list' : frametimeErrorData})
frametimeErrorDataFrame.to_csv('Frametime-Error.csv')

gpuTimeErrorDataFrame = pd.DataFrame({'GPUTime error list' : gpuTimeErrorData})
gpuTimeErrorDataFrame.to_csv('GPUTime-error.csv')

print("\n\nDone! Missed Frame:", missedFrame)
print("Frametime error:", + frametimeError)
print("GPUTime error:", + gpuTimeError)