from constant_func import *

"""
메인 GUI 파싱 데이터에 접근할때 사용되는 keys
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
툴바 함수 관리 키
"""

# AvoidDuplicateCreation - CBValueSave
CBValueSave_Func = "CBValueSave-Func"
CBValueSave_FileSaved = "CBValueSave-FileSaved"


""" 
툴바 설정 키-값 정의
"""

# settings_LBL_CB
Preview_data = "Preview data"
Preview_data_parmeters = ("used", "not used")
Preview_data_default = 0

Startup_mode = "Startup mode"
Startup_mode_parmeters = ("speed mode", "stability mode")
Startup_mode_default = 1


Font_Changed = "Font changed (Restart required)"
Font_Changed_parmeters = Font_Read("Fonts/Open_Sans/static")
Font_Changed_default = 0


""" 
URL 경로 관리
"""

# 폰트 경로
font_path = Font_path("Settings/Settings.json", Font_Changed) # 폰트 파일 경로

# 설정 경로
SettingsWritePath = get_absolute_path("Settings/%s")

# Toolbar FilePath
SettingFilePath = get_absolute_path("Settings/Settings_LBL_CB.json")
ButtonFilePath = get_absolute_path("Settings/Settings_BTN.json")
SetDataFilePath = get_absolute_path("Settings/Settings.json")

# Icon FilePath
# "/" 를 사용해야 합니다.
DouSBUpIConFilePath = get_absolute_path("icons/up-arrow(DoubleSpinBox).png")
DouSBDownIConFilePath = get_absolute_path("icons/down-arrow(DoubleSpinBox).png")
CBDownIconFilePath = get_absolute_path("icons/down-arrow(ComboBox).png")

# logging FilePath
FolderPath = MakeFolder(f"debugs/{CurrentTime()}")