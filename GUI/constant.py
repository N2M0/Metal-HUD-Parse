
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

# Toolbar FilePath
SettingFilePath = r"GUI\Settings\Settings_LBL_CB.json"
ButtonFilePath = r"GUI\Settings\Settings_BTN.json"
SetDataFilePath = r"GUI\Settings\Settings.json"

# Icon FilePath
DouSBUpIConFilePath = "GUI/icons/up-arrow(DoubleSpinBox).png"
DouSBDownIConFilePath = "GUI/icons/down-arrow(DoubleSpinBox).png"
CBDownIconFilePath = "GUI/icons/down-arrow(ComboBox).png"

""" 
상수, 툴바 함수 관리 키
"""

# AvoidDuplicateCreation - CBValueSave
CBValueSave_Func = "CBValueSave-Func"
CBValueSave_FileSaved = "CBValueSave-FileSaved"