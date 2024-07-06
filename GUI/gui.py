import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGridLayout, QFrame, QSpacerItem, QSizePolicy, QDoubleSpinBox, QAbstractSpinBox
from PyQt5.QtCore import Qt, QTimer
from Metal_HUD_parse import *
from gui_style import *
from gui_thread import *
from FileRead import *
from CustomQDoubleSpinBox import *

class MetalHUDParse(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 윈도우 설정
        self.setWindowTitle('My PyQt5 Window')
        self.resize(1400, 800)
        
        # 레이아웃 생성
        self.Mainvbox = QVBoxLayout()
        
        # 파일 리드
        self.FileReadframe = self.FileReadWindow()
        self.Mainvbox.addWidget(self.FileReadframe)
        
        
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
        self.FileLabel.setStyleSheet(LabelStyle(FileLabelType+"#"+FileLabelObjID))
        self.FileLabel.setAlignment(Qt.AlignCenter)
        
        # 파일 버튼 생성
        self.FileReadBtn = QPushButton('File Read')
        FileButtonType, FileButtonObjID = "QPushButton", "FileReadBtn"
        self.FileReadBtn.setObjectName(FileButtonObjID)
        self.FileReadBtn.setStyleSheet(ButtonStyle(FileButtonType+"#"+FileButtonObjID))
        self.FileReadBtn.setFixedSize(200, 80)
        self.FileReadBtn.clicked.connect(lambda: FileReader(self).FileRead())

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
        
        # 성능 라벨 생성
        self.StartPerformanceLable = QLabel("Metal HiD Parse")
        StartPerformanceLabelType, StartPerformanceLabelObjID = "QLabel", "StartPerformanceLable"
        self.StartPerformanceLable.setObjectName(StartPerformanceLabelObjID)
        self.StartPerformanceLable.setStyleSheet(LabelStyle(StartPerformanceLabelType+"#"+StartPerformanceLabelObjID))
        self.StartPerformanceLable.setAlignment(Qt.AlignCenter)
        
        # 단위 변환
        self.UnitConversion = CustomQDoubleSpinBox(self).QDSpinBox(
            setRnage=(0, 10000),
            setSingleStep=1,
            setValue=1000,
            setFixedSize=(100, 50),
            setStyleSheet=QDoubleSpinBoxStyle(),
            setDecimals=0,
            setButtonSymbols=QAbstractSpinBox.NoButtons,
            setAlignment=Qt.AlignCenter            
        )

        # 소수점 제한
        self.DecimalPoint = CustomQDoubleSpinBox(self).QDSpinBox(
            setRnage=(0, 10000),
            setSingleStep=1,
            setValue=2,
            setFixedSize=(100, 50),
            setStyleSheet=QDoubleSpinBoxStyle(),
            setDecimals=0,
            setButtonSymbols=QAbstractSpinBox.NoButtons,
            setAlignment=Qt.AlignCenter            
        )
        
        # 성능 버튼 생성
        self.ParseStartBtn = QPushButton('Parse Start')
        ParseStartType, ParseStartObjID = "QPushButton", "ParseStartBtn"
        self.ParseStartBtn.setObjectName(ParseStartObjID)
        self.ParseStartBtn.setStyleSheet(ButtonStyle(ParseStartType+"#"+ParseStartObjID))
        self.ParseStartBtn.setFixedSize(200, 80)
        self.ParseStartBtn.clicked.connect(lambda: self.StartParsePerformance(FileName, DataReader(FileName)))
        
        StartPerformancevbox.addWidget(self.StartPerformanceLable, alignment=Qt.AlignTop)
        StartPerformancevbox.addWidget(self.UnitConversion, alignment=Qt.AlignLeft | Qt.AlignHCenter)
        StartPerformancevbox.addWidget(self.DecimalPoint, alignment=Qt.AlignLeft | Qt.AlignHCenter)
        StartPerformancevbox.addWidget(self.ParseStartBtn, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        StartPerformanceframe.setLayout(StartPerformancevbox)
        
        return StartPerformanceframe

    def StartParsePerformance(self, FileName, FileData):
        self.thread = PerformanceParsingThread(FileName, FileData, 1000, 2)
        self.thread.UpdateFileLabelSignal.connect(lambda text: self.StartPerformanceLable.setText(text))
        self.thread.ThreadFinishedSignal.connect(lambda: QTimer.singleShot(1000, lambda: None))
        self.thread.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MetalHUDParse()
    window.show()
    sys.exit(app.exec_())
