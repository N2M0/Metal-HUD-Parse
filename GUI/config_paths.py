from config_paths_Utils import *

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
메인 GUI 여러작업의 실행 여부를 결정하는 Keys.
"""
parse_thread_state = "parse_thread_state"


""" 
툴바 설정 키-값 정의
"""

# settings_LBL_CB
# 미리보기 테이블 및 프로그래스바 사용 여부
Preview_data = "Preview data"
Preview_data_parmeters = ("used", "not used")
Preview_data_default = 0

# 미리보기 테이블 보기 모드
Preview_data_viewing_mode = "Preview data viewing mode"
Preview_data_viewing_mode_parmeters = ("Raw mode", "statistical mode")
Preview_data_viewing_mode_default = 0

# 시작시 성능 모드
Startup_mode = "Startup mode"
Startup_mode_parmeters = ("speed mode", "stability mode")
Startup_mode_default = 1

# 폰트 변경
Font_Changed = "Font changed (Restart required)"
Font_Changed_parmeters = Font_Read("Fonts/Open_Sans/static")
Font_Changed_default = 0

# Parse 파일 데이터에 인덱스 포함
Include_Index_In_File_Parse_data = "Include Index In File Parse data"
Include_Index_In_File_Parse_data_parameters = ("Displayed", "Not Displayed")
Include_Index_In_File_Parse_data_default = 0

""" 
URL/경로 관리
"""

# "/" 를 사용해야 합니다.

# 폰트 경로
font_path = Font_Path("Settings/Settings.json", Font_Changed) # 폰트 파일 경로

# 설정 경로
SettingsWritePath = get_absolute_path("Settings/%s")

# Toolbar FilePath
SettingFilePath = get_absolute_path("Settings/Settings_LBL_CB.json")
ButtonFilePath = get_absolute_path("Settings/Settings_BTN.json")
SetDataFilePath = get_absolute_path("Settings/Settings.json")

# Icon FilePath
DouSBUpIConFilePath = get_absolute_path("icons/up-arrow(DoubleSpinBox).png")
DouSBDownIConFilePath = get_absolute_path("icons/down-arrow(DoubleSpinBox).png")
CBDownIconFilePath = get_absolute_path("icons/down-arrow(ComboBox).png")

# logging FilePath
FolderPath = MakeFolder(f"debugs/{CurrentTime()}")

# Parse Data Save FilePath / 해당 폴더 패치는 여기에 표시만 합니다. 
# 저장을 할때마다 폴더가 새로 생성돼야 하기 때문에 파일 세이브 스레드 영역에 폴더 패치 코드를 작성했습니다.
# ParseDataSavePath = MakeFolder(f"Parse_Save/{CurrentTime()}")
