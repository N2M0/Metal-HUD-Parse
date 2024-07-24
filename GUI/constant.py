import os

"""
상수, 메인 GUI 파싱 데이터에 접근할때 사용되는 keys
"""

# PerformanceCalculationConditions
benchmarkBasedTime = "benchmarkBasedTime"
missedFrame = "missedFrame"
frametimeError = "frametimeError"
gpuTimeError = "gpuTimeError"
secondSum = "secondSum"
frameCount = "frameCount"
overlapCheckData = "overlapCheckData"

# PerformanceData
FPSData = "FPSData"
frameTimeData = "frameTimeData"
gpuTimeData = "gpuTimeData"
memoryData = "memoryData"

# PerformanceErrorData
frametimeErrorData = "frametimeErrorData"
gpuTimeErrorData = "gpuTimeErrorData"


""" 
상수, URL 경로 관리
"""


# 파일 존재 여부 확인 함수
def check_file_exists(file_path):
    # 스크립트 파일의 디렉토리 경로 가져오기
    base_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_path, file_path).replace('\\', '/')

# Toolbar FilePath
SettingFilePath = check_file_exists("Settings/Settings_LBL_CB.json")
ButtonFilePath = check_file_exists("Settings/Settings_BTN.json")
SetDataFilePath = check_file_exists("Settings/Settings.json")

# Icon FilePath
# "/" 를 사용해야 합니다.
DouSBUpIConFilePath = check_file_exists("icons/up-arrow(DoubleSpinBox).png")
DouSBDownIConFilePath = check_file_exists("icons/down-arrow(DoubleSpinBox).png")
CBDownIconFilePath = check_file_exists("icons/down-arrow(ComboBox).png")


""" 
상수, 툴바 함수 관리 키
"""

# AvoidDuplicateCreation - CBValueSave
CBValueSave_Func = "CBValueSave-Func"
CBValueSave_FileSaved = "CBValueSave-FileSaved"


""" 
상수, 툴바 설정 키-값 정의
"""

# settings_LBL_CB
Preview_data = "Preview data"
Preview_data_parmeters = ("used", "not used")
Preview_data_default = 0

Startup_mode = "Startup mode"
Startup_mode_parmeters = ("speed mode", "stability mode")
Startup_mode_default = 1