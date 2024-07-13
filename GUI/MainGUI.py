import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QTableWidget, QTableWidgetItem, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from Metal_HUD_parse import *
from GUIStyle import *
from GUIThread import *
from FileRead import *
from CustomQDSpin import *
from ToolBar import *

class MetalHUDParse(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 윈도우 설정
        self.setWindowTitle('Metal-HUD Parse')
        self.resize(1400, 800)
        
        # 레이아웃 생성
        self.Mainvbox = QVBoxLayout()
        
        # 파일 리드
        self.FileReadframe = self.FileReadWindow()
        self.Mainvbox.addWidget(self.FileReadframe)
        self.FileReader = FileReader(self)

        # 포커스 정책 설정
        self.setFocusPolicy(Qt.StrongFocus)
        
        # 레이아웃 설정
        self.setLayout(self.Mainvbox)

    # 처음 실행시 최초화면
    def FileReadWindow(self):
        FileReadframe = QFrame()
        FileReadframe.setFrameShape(QFrame.Panel | QFrame.Sunken)
        FileReadvbox = QVBoxLayout()
        
        # 설정툴바
        self.settings_toolbar = SettingsToolbar(self)

        # 파일 라벨 생성
        self.FileLabel = QLabel("Load The File.")
        FileLabelType, FileLabelObjID = "QLabel", "FileLabel"
        self.FileLabel.setObjectName(FileLabelObjID)
        self.FileLabel.setStyleSheet(LabelStyle(FileLabelType+"#"+FileLabelObjID, 25))
        self.FileLabel.setAlignment(Qt.AlignCenter)
        
        # 파일 버튼 생성
        self.FileReadBtn = QPushButton('File Read')
        FileButtonType, FileButtonObjID = "QPushButton", "FileReadBtn"
        self.FileReadBtn.setObjectName(FileButtonObjID)
        self.FileReadBtn.setStyleSheet(ButtonStyle(FileButtonType+"#"+FileButtonObjID))
        self.FileReadBtn.setFixedSize(200, 80)
        self.FileReadBtn.clicked.connect(lambda: self.FileReader.FileRead())

        # 라벨과 버튼을 중앙에 배치
        FileReadvbox.addWidget(self.settings_toolbar, alignment=Qt.AlignTop)
        FileReadvbox.addStretch(1)
        FileReadvbox.addWidget(self.FileLabel, alignment=Qt.AlignCenter)
        FileReadvbox.addSpacing(20)  # 라벨과 버튼 사이의 여백
        FileReadvbox.addWidget(self.FileReadBtn, alignment=Qt.AlignCenter)
        FileReadvbox.addStretch(1)
        
        FileReadframe.setLayout(FileReadvbox)
        
        return FileReadframe
    
    # 처음화면에서 파일 선택시 이동화면
    def StartPerformanceWindow(self, FileName):
        # 인스턴스 변수
        self.FileName = FileName

        # 설정툴바
        self.settings_toolbar = SettingsToolbar(self)

        # 성능 라벨 생성
        self.StartPerformanceLable = QLabel("Metal-HUD Parse")
        StartPerformanceLabelType, StartPerformanceLabelObjID = "QLabel", "StartPerformanceLable"
        self.StartPerformanceLable.setObjectName(StartPerformanceLabelObjID)
        self.StartPerformanceLable.setStyleSheet(LabelStyle(StartPerformanceLabelType+"#"+StartPerformanceLabelObjID, 25))
        self.StartPerformanceLable.setAlignment(Qt.AlignCenter)
        
        
        # 스핀박스 이름 변경필요. 
        
        # 벤치마크 베이스 시간
        self.benchmarkBasedTime, self.benchmarkBasedTimeLabel = self.addQDSpinBox(1000, "Average milliseconds")
        # 단위 변환
        self.UnitConversion, self.UnitConversionLabel = self.addQDSpinBox(1000, "Unit conversion")
        # 소수점 제한
        self.DecimalPoint, self.DecimalPointLabel = self.addQDSpinBox(2, "decimal point")
        
        # 테이블 초기화
        self.ParsedResultsTable = self.InitParsedTable()
        
        # 프로그래스바 초기화
        self.ParsedPbar = self.InitQProgressBar()
        
        # 데이터 파싱 버튼 초기화
        self.ParseStartBtn = self.addBtn(
            "Parse Start", 
            lambda: self.StartParsePerformance(
            self.FileName, 
            DataReader(self.FileName), 
            int(self.benchmarkBasedTime.value()), 
            int(self.UnitConversion.value()), 
            int(self.DecimalPoint.value())),
            )
        
        # 파일 변경 버튼 초기화
        self.FileChange = self.addBtn("File Change", self.FileChanged)
        
        # 결과를 파일로 저장 버튼 초기화
        self.ParsedSave = self.addBtn("Parsed Save", lambda: PerformanceParsingResultsSaveThread(self).run())
        
        # 위 객체들을 레이아웃에 추가하는 함수 초기화
        StartPerformanceframe = self.addlayout()
        
        return StartPerformanceframe
    
    
    # StartPerformanceWindow 의 객체를 레이아웃에 추가해주는 함수
    def addlayout(self):
        StartPerformanceframe = QFrame()
        StartPerformanceframe.setFrameShape(QFrame.Panel | QFrame.Sunken)
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
            self.UnitConversion: self.UnitConversionLabel,
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


    # 파일 이름 변경 함수
    def FileChanged(self):
        f = self.FileReader.FileChanged()
        if f is not None:
            self.FileName = f

    # 버튼 추가 함수
    def addBtn(self, BtnName, func):
        _addbtn = QPushButton(BtnName)
        _addbtnType, _addbtnObjID = "QPushButton", "AddBtn"
        _addbtn.setObjectName(_addbtnObjID)
        _addbtn.setStyleSheet(ButtonStyle(_addbtnType+"#"+_addbtnObjID))
        _addbtn.setFixedSize(200, 80)
        _addbtn.clicked.connect(func)
        
        return _addbtn
    
    # 스핀박스 추가 함수
    def addQDSpinBox(self, setValue, LabelText):
        QDSpinObj = CustomQDoubleSpinBox(self).QDSpinBox(
            setRange=(0, 10000000),
            setSingleStep=1,
            setValue=setValue,
            setFixedSize=(120, 60),
            setStyleSheet=QDoubleSpinBoxStyle(),
            setDecimals=0,
            setAlignment=Qt.AlignCenter            
        )
        
        QDSpinObjLabel = CustomQDSpinBoxLabel(self).QDSpinBoxLabel(
            LabelText=LabelText,
            setStyleSheet=LabelStyle
            
        )
        
        return QDSpinObj, QDSpinObjLabel

    # 데이터 미리보기 표시
    def InitParsedTable(self):
        self.ParsedTable = QTableWidget(self)
        self.ParsedTable.setFixedSize(1400, 300)
        
        return self.ParsedTable

    # 프로그래스바 표시
    def InitQProgressBar(self):
        pbar = QProgressBar(self)
        pbar.setFixedSize(int(1400 // 1.5) - 200, 30)
        pbar.setStyleSheet(PbarStyle())
        # 숫자값의 위치
        pbar.setAlignment(Qt.AlignCenter)
        pbar.resetFormat()

        return pbar

    # 스레도 함수
    def StartParsePerformance(self, FileName, FileData, benchmarkBasedTime, UnitConversion, DecimalPoint):
        self.LayWorker = LayUpdateWorker(self, FileName, FileData, benchmarkBasedTime, UnitConversion, DecimalPoint)
        self.LayWorker.start()


# 메인 레이아웃을 업데이트 하기 위한 클래스, 코드의 가독성을 위해 클래스로 분리함.
class LayUpdateWorker(QWidget):
    def __init__(self, parent, FileName, FileData, benchmarkBasedTime, UnitConversion, DecimalPoint):
        super(LayUpdateWorker, self).__init__(parent)
        self.parent = parent
        self.StartPerformanceLable = self.parent.StartPerformanceLable
        self.ParsedResultsTable = self.parent.ParsedResultsTable
        self.ParsedPbar = self.parent.ParsedPbar
        
        # 인스턴스 변수
        self.FileName = FileName
        self.FileData = FileData
        self.benchmarkBasedTime = benchmarkBasedTime
        self.UnitConversion = UnitConversion
        self.DecimalPoint = DecimalPoint
        
    def start(self):
        self.thread = PerformanceParsingThread(self.parent, self.FileName, self.FileData, self.benchmarkBasedTime, self.UnitConversion, self.DecimalPoint)
        self.thread.UpdateFileLabelSignal.connect(lambda text: self.StartPerformanceLable.setText(text))
        self.thread.EmitInitializeTableSignal.connect(self.InitializeTable)
        self.thread.EmitParsedSignal.connect(self.UpdateTable)
        self.thread.EmitParsedPbarSignal.connect(self.UpdateProgressBar)
        self.thread.ThreadFinishedSignal.connect(lambda: QTimer.singleShot(1000, self.UpdateTableResizeContents))
        self.thread.start()

    # 테이블 초기화
    def InitializeTable(self, label_list, col_count, row_count):
        self.ParsedResultsTable.setColumnCount(0)    
        self.ParsedResultsTable.setRowCount(0)
        self.ParsedResultsTable.setColumnCount(col_count)
        self.ParsedResultsTable.setRowCount(row_count)
        self.ParsedResultsTable.setHorizontalHeaderLabels(label_list)
        
    # 테이블 업데이트 함수
    def UpdateTable(self, col, row, value):
        # 테이블에 데이터를 추가
        item = QTableWidgetItem(value)
        item.setTextAlignment(Qt.AlignCenter)  # 텍스트 정렬 (옵션)
        self.ParsedResultsTable.setItem(row, col, item)
    
    def UpdateTableResizeContents(self):
        # 테이블 전체 크기 조정
        self.ParsedResultsTable.resizeColumnsToContents() # 행
        self.ParsedResultsTable.resizeRowsToContents() # 열
    
    # 프로그래스바 업데이트 함수
    def UpdateProgressBar(self, sum_pbar, sum_count):
        progress = (sum_pbar / sum_count) * 100  # 프로그래스바 계산
        self.ParsedPbar.setValue(int(progress))  # 프로그래스바 업데이트
        
        if progress >= sum_count:
            self.ParsedPbar.setValue(0)  # 파싱을 재실행하면 프로그래스바 진행상황을 초기화


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MetalHUDParse()
    window.show()
    sys.exit(app.exec_())
