import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget, 
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QHBoxLayout,
    QTableWidget,
    QProgressBar
    )

from PyQt5.QtCore import Qt
from GUIStyle import *
from GUIThread import *
from FileUIManager import *
from CustomQDSpin import *
from ToolBar import *
from SavedWorker import *
from LayWorker import *
from config_paths import *
from Json_Utils import *
from applog import *

logger = InitLogger(CurrentFileName(__file__))

class MetalHUDParse(QWidget):
    def __init__(self):
        super().__init__()
        logger.info("프로그램 시작")  # 프로그램 시작 시 메시지

        # 종료 시그널에 슬롯 연결
        self.closeEvent = self.on_close
        
        self._name = __class__.__name__
        # 특정 폴더에 있는 폰트 로드
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        self.InitUI()

    def InitUI(self):
        try:
            # 윈도우 설정
            # 창 크기 값을 변수로 관리 권장.
            self.setWindowTitle('Metal-HUD Parse')
            
            self._width, self._height = 1200, 800
            self.setMinimumSize(self._width, self._height) # 창 크기 고정
            
            # 레이아웃 생성
            self.Mainvbox = QVBoxLayout()
            
            # 파일 리드
            self.FileReadframe = self.FileReadWindow()
            self.Mainvbox.addWidget(self.FileReadframe)
            self.FileUIManager = FileUIManager(self)

            # 포커스 정책 설정
            self.setFocusPolicy(Qt.StrongFocus)
            
            # 레이아웃 설정
            self.setLayout(self.Mainvbox)

        except Exception as e:
            logger.error(f"{self._name} - 메인 화면을 초기화하는 과정에 문제가 생겼습니다. | Error Code: {e}")

    # 처음 실행시 최초화면
    def FileReadWindow(self):
        try:
            # 설정툴바
            self.settings_toolbar = SettingsToolbar(self)

            # 파일 라벨 생성
            self.FileLabel = QLabel("Load The File.")
            FileLabelType, FileLabelObjID = "QLabel", "FileLabel"
            self.FileLabel.setObjectName(FileLabelObjID)
            self.FileLabel.setStyleSheet(LabelStyle(FileLabelType+"#"+FileLabelObjID, self.font_family, 25))
            self.FileLabel.setAlignment(Qt.AlignCenter)
            
            # 파일 버튼 생성
            self.FileReadBtn = QPushButton('File Read')
            FileButtonType, FileButtonObjID = "QPushButton", "FileReadBtn"
            self.FileReadBtn.setObjectName(FileButtonObjID)
            self.FileReadBtn.setStyleSheet(ButtonStyle(FileButtonType+"#"+FileButtonObjID, self.font_family))
            self.FileReadBtn.setMinimumSize(200, 80)
            self.FileReadBtn.clicked.connect(lambda: self.FileUIManager.FileRead())

            FileReadframe = self.FileReadWindow_Layout()
            return FileReadframe
            

        except Exception as e:
            logger.error(f"{self._name} - 파일 불러오기 화면의 문제가 생겼습니다. | Error Code: {e}")
            return None
    
    # FileReadWindow 의 객체를 레이아웃에 추가해주는 함수
    def FileReadWindow_Layout(self):
        try:
            FileReadframe = QFrame()
            FileReadvbox = QVBoxLayout()
            
            # 라벨과 버튼을 중앙에 배치
            FileReadvbox.addWidget(self.settings_toolbar, alignment=Qt.AlignTop)
            FileReadvbox.addStretch(1)
            FileReadvbox.addWidget(self.FileLabel, alignment=Qt.AlignCenter)
            FileReadvbox.addSpacing(20)  # 라벨과 버튼 사이의 여백
            FileReadvbox.addWidget(self.FileReadBtn, alignment=Qt.AlignCenter)
            FileReadvbox.addStretch(1)
            
            FileReadframe.setLayout(FileReadvbox)
            
            return FileReadframe
        
        except Exception as e:
            logger.error(f"{self._name} - 파일 불러오기 화면의 레이아웃 또는 위젯을 추가하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            return None
        
    # 처음화면에서 파일 선택시 이동화면
    def StartPerformanceWindow(self, FileName):
        try:
            # 인스턴스 변수
            self.FileName = FileName

            # 설정툴바
            self.settings_toolbar = SettingsToolbar(self)

            # 성능 라벨 생성
            self.StartPerformanceLable = QLabel("Metal-HUD Parse")
            StartPerformanceLabelType, StartPerformanceLabelObjID = "QLabel", "StartPerformanceLable"
            self.StartPerformanceLable.setObjectName(StartPerformanceLabelObjID)
            self.StartPerformanceLable.setStyleSheet(LabelStyle(StartPerformanceLabelType+"#"+StartPerformanceLabelObjID, self.font_family, 25))
            self.StartPerformanceLable.setAlignment(Qt.AlignCenter)
            
            # 벤치마크 베이스 시간
            self.benchmarkBasedTime, self.benchmarkBasedTimeLabel = self.addQDSpinBox(1000, "Average Milliseconds")

            # 소수점 제한
            self.DecimalPoint, self.DecimalPointLabel = self.addQDSpinBox(2, "Decimal Point")
            
            # 테이블 초기화
            self.ParsedResultsTable = self.InitParsedTable()
            
            # 프로그래스바 초기화
            self.ParsedPbar = self.InitQProgressBar()
            
            # 데이터 파싱 버튼 초기화
            self.ParseStartBtn = self.addBtn(
                "Parse Start", 
                lambda: self.StartParsePerformance(
                self.FileName,
                int(self.benchmarkBasedTime.value()),
                int(self.DecimalPoint.value())),
                )
            
            # 파일 변경 버튼 초기화
            self.FileChange = self.addBtn("File Change", self.FileChanged)
            
            # 결과를 파일로 저장 버튼 초기화
            self.ParsedSave = self.addBtn("Parsed Save", self.StartParsePerformanceSave)
            
            # 위 객체들을 레이아웃에 추가하는 함수 초기화
            StartPerformanceframe = self.StartPerformanceWindow_layout()
            
            # 툴바 설정 값에 의해 숨김 처리된 위젯 초기값.
            self.widget_Hide()
            
            return StartPerformanceframe
        
        except Exception as e:
            logger.error(f"{self._name} - 시작 성능 화면의 문제가 생겼습니다. | Error Code: {e}")
            return None
    
    # StartPerformanceWindow 의 객체를 레이아웃에 추가해주는 함수
    def StartPerformanceWindow_layout(self):
        try:
            StartPerformanceframe = QFrame()
            StartPerformancevbox = QVBoxLayout()
            StartPerformancehbox = QHBoxLayout()

            # 수직
            StartPerformancevbox.addWidget(self.settings_toolbar, alignment=Qt.AlignLeft)
            StartPerformancevbox.addWidget(self.ParsedResultsTable, alignment= Qt.AlignCenter)
            StartPerformancevbox.addSpacing(10) # 여백
            StartPerformancevbox.addWidget(self.ParsedPbar, alignment = Qt.AlignHCenter)
            StartPerformancevbox.addSpacing(10) # 여백
            StartPerformancevbox.addWidget(self.StartPerformanceLable, alignment=Qt.AlignCenter)
            
            # 수직 스핀박스
            # 키-값 정의
            SpinDict = {
                self.benchmarkBasedTime: self.benchmarkBasedTimeLabel,
                self.DecimalPoint: self.DecimalPointLabel
            }
            StartPerformancevbox.addStretch(1)
            for object, label in SpinDict.items():
                StartPerformancevbox.addWidget(label, alignment=Qt.AlignLeft | Qt.AlignHCenter)
                StartPerformancevbox.addSpacing(5) # 여백
                StartPerformancevbox.addWidget(object, alignment=Qt.AlignLeft | Qt.AlignHCenter)
                StartPerformancevbox.addSpacing(20) # 여백
            StartPerformancevbox.addStretch(1)
            
            
            # 수평
            StartPerformancehbox.addStretch(1)
            StartPerformancehbox.addWidget(self.ParseStartBtn, alignment=Qt.AlignBottom | Qt.AlignHCenter)
            StartPerformancehbox.addSpacing(10) # 여백
            StartPerformancehbox.addWidget(self.FileChange, alignment=Qt.AlignBottom | Qt.AlignHCenter)
            StartPerformancehbox.addSpacing(10) # 여백
            StartPerformancehbox.addWidget(self.ParsedSave, alignment=Qt.AlignBottom | Qt.AlignHCenter)
            StartPerformancehbox.addStretch(1)

            # 레이아웃 추가
            StartPerformancevbox.addLayout(StartPerformancehbox)
            StartPerformanceframe.setLayout(StartPerformancevbox)
            
            return StartPerformanceframe

        except Exception as e:
            logger.error(f"{self._name} - 시작 성능 화면의 레이아웃 또는 위젯을 추가하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            return None

    def widget_Hide(self):
        # 설정 값 가져오기
        settings = OpenJson(SetDataFilePath)
        if not settings[Preview_data] == Preview_data_parmeters[Preview_data_default]:
            self.ParsedResultsTable.hide()
            self.ParsedPbar.hide()


    # 파일 이름 변경 함수
    def FileChanged(self):
        try:
            f = self.FileUIManager.FileChanged()
            if f is not None:
                self.FileName = f
                
        except Exception as e:
            logger.error(f"{self._name} - 파일을 변경하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            return None

    # 버튼 추가 함수
    def addBtn(self, BtnName, func):
        try:
            _addbtn = QPushButton(BtnName)
            _addbtnType, _addbtnObjID = "QPushButton", "AddBtn"
            _addbtn.setObjectName(_addbtnObjID)
            _addbtn.setStyleSheet(ButtonStyle(_addbtnType+"#"+_addbtnObjID, self.font_family))
            _addbtn.setMinimumSize(190, 70)
            _addbtn.clicked.connect(func)
            
            return _addbtn

        except Exception as e:
            logger.error(f"{self._name} - 정의된 버튼 함수에 문제가 생겼습니다. | Error Code: {e}")
            return None
    
    # 스핀박스 추가 함수
    def addQDSpinBox(self, setValue, LabelText):
        try:
            QDSpinObj = CustomQDoubleSpinBox(self).QDSpinBox(
                setRange=(0, 10000000),
                setSingleStep=1,
                setValue=setValue,
                setMinimumSize=(120, 55),
                setDecimals=0,
                setAlignment=Qt.AlignCenter            
            )
            
            QDSpinObjLabel = CustomQDSpinBoxLabel(self).QDSpinBoxLabel(
                LabelText=LabelText
            )
            
            return QDSpinObj, QDSpinObjLabel

        except Exception as e:
            logger.error(f"{self._name} - 정의된 스핀박스 함수에 문제가 생겼습니다. | Error Code: {e}")
            return None, None
        
    # 데이터 미리보기 표시
    def InitParsedTable(self):
        try:
            ParsedTable = QTableWidget(self)
            ParsedTable.setMinimumSize(self._width - 80, 300)
            
            return ParsedTable
        except Exception as e:
            logger.error(f"{self._name} - 미리보기 테이블을 추가하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            return None
            
    # 프로그래스바 표시
    def InitQProgressBar(self):
        try:
            pbar = QProgressBar(self)
            pbar.setMinimumSize(int(self._width // 1.5) - 100, 30)
            pbar.setStyleSheet(PbarStyle(self.font_family))
            # 숫자값의 위치
            pbar.setAlignment(Qt.AlignCenter)

            return pbar
        
        except Exception as e:
            logger.error(f"{self._name} - 프로그래스바를 추가하는 과정에 문제가 생겼습니다. | Error Code: {e}")
            return None
        
    # 스레드 함수
    def StartParsePerformance(self, FileName, benchmarkBasedTime, DecimalPoint):
        try:
            # 파스 결과를 메인 레이아웃에 업데이트하는 객체
            LayWorker = LayUpdateWorker(self, FileName, benchmarkBasedTime, DecimalPoint)
            LayWorker.start()
            
        except Exception as e:
            logger.error(f"{self._name} - Parse 관련 레이아웃 업데이트 클래스에 문제가 생겼습니다. | Error Code: {e}")
            
    def StartParsePerformanceSave(self):
        try:
            SaveWorked = ParsedDataSavedWorker(self)
            SaveWorked.start()
            
        except Exception as e:
            logger.error(f"{self._name} - Parsed Data를 저장하는 클래스에 문제가 생겼습니다. | Error Code: {e}")

    # 종료 이벤트
    def on_close(self, event):
        logger.info("프로그램 종료")  # 종료 시 메시지
        event.accept()  # 종료 이벤트를 수락

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MetalHUDParse()
    window.show()
    sys.exit(app.exec_())