import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGridLayout, QFrame, QHBoxLayout, QAbstractSpinBox
from PyQt5.QtCore import Qt, QTimer
from Metal_HUD_parse import *
from gui_style import *
from gui_thread import *
from FileRead import *
from CustomQDSpin import *

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
        
        # 레이아웃 설정
        self.setLayout(self.Mainvbox)


    def FileReadWindow(self):
        FileReadframe = QFrame()
        FileReadframe.setFrameShape(QFrame.Panel | QFrame.Sunken)
        FileReadvbox = QVBoxLayout()
        
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
        FileReadvbox.addStretch(1)
        FileReadvbox.addWidget(self.FileLabel, alignment=Qt.AlignCenter)
        FileReadvbox.addSpacing(20)  # 라벨과 버튼 사이의 여백
        FileReadvbox.addWidget(self.FileReadBtn, alignment=Qt.AlignCenter)
        FileReadvbox.addStretch(1)
        
        FileReadframe.setLayout(FileReadvbox)
        
        return FileReadframe
    
    
    def StartPerformanceWindow(self, FileName):
        StartPerformanceframe = QFrame()
        StartPerformanceframe.setFrameShape(QFrame.Panel | QFrame.Sunken)
        StartPerformancevbox = QVBoxLayout()
        StartPerformancehbox = QHBoxLayout()
        self.FileName = FileName

        
        # 성능 라벨 생성
        self.StartPerformanceLable = QLabel("Metal HiD Parse")
        StartPerformanceLabelType, StartPerformanceLabelObjID = "QLabel", "StartPerformanceLable"
        self.StartPerformanceLable.setObjectName(StartPerformanceLabelObjID)
        self.StartPerformanceLable.setStyleSheet(LabelStyle(StartPerformanceLabelType+"#"+StartPerformanceLabelObjID, 25))
        self.StartPerformanceLable.setAlignment(Qt.AlignCenter)
        
        # 벤치마크 베이스 시간
        self.benchmarkBasedTime, self.benchmarkBasedTimeLabel = self.addQDSpinBox(1000, "BasedTime")
        # 단위 변환
        self.UnitConversion, self.UnitConversionLabel = self.addQDSpinBox(1000, "UnitConversion")
        # 소수점 제한
        self.DecimalPoint, self.DecimalPointLabel = self.addQDSpinBox(2, "DecimalPoint")
        
        # spinbox dict
        SpinDict = {
            self.benchmarkBasedTime: self.benchmarkBasedTimeLabel,
            self.UnitConversion: self.UnitConversionLabel,
            self.DecimalPoint: self.DecimalPointLabel
        }
        
        # 성능 버튼 생성
        self.ParseStartBtn = self.addBtn(
            "Parse Start", 
            lambda: self.StartParsePerformance(
            self.FileName, 
            DataReader(self.FileName), 
            int(self.benchmarkBasedTime.value()), 
            int(self.UnitConversion.value()), 
            int(self.DecimalPoint.value()))
            )
        
        # FileChange 버튼 생성
        self.FileChange = self.addBtn("File Change", self.FileChanged)
        # 수직
        StartPerformancevbox.addWidget(self.StartPerformanceLable, alignment=Qt.AlignTop)
        
        # 수직 스핀박스
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
        StartPerformancehbox.addSpacing(20) # 여백
        StartPerformancehbox.addWidget(self.FileChange, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        StartPerformancehbox.addStretch(1)
        StartPerformancevbox.addLayout(StartPerformancehbox)
        StartPerformanceframe.setLayout(StartPerformancevbox)
        
        return StartPerformanceframe
    
    # 파일 이름 변경 함수
    def FileChanged(self):
        self.FileName = self.FileReader.FileChanged()

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
            setRange=(0, 1000000),
            setSingleStep=1,
            setValue=setValue,
            setFixedSize=(100, 50),
            setStyleSheet=QDoubleSpinBoxStyle(),
            setDecimals=0,
            setButtonSymbols=QAbstractSpinBox.NoButtons,
            setAlignment=Qt.AlignCenter            
        )
        
        QDSpinObjLabel = CustomQDSpinBoxLabel(self).QDSpinBoxLabel(
            LabelText=LabelText,
            setStyleSheet=LabelStyle
            
        )
        
        return QDSpinObj, QDSpinObjLabel

    # 스레도 함수
    def StartParsePerformance(self, FileName, FileData, benchmarkBasedTime, UnitConversion, DecimalPoint):
        self.thread = PerformanceParsingThread(FileName, FileData, benchmarkBasedTime, UnitConversion, DecimalPoint)
        self.thread.UpdateFileLabelSignal.connect(lambda text: self.StartPerformanceLable.setText(text))
        self.thread.ThreadFinishedSignal.connect(lambda: QTimer.singleShot(1000, lambda: None))
        self.thread.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MetalHUDParse()
    window.show()
    sys.exit(app.exec_())
