from PyQt5.QtWidgets import QLabel, QDoubleSpinBox
from PyQt5.QtCore import Qt
from Metal_HUD_parse import *
from GUIStyle import *
from constant import *

# 스핀박스를 구성하는 클래스
class CustomQDoubleSpinBox:
    def __init__(self, parent):
        self._name = __class__.__name__
        
        # 특정 폴더에 있는 폰트 로드
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        self.parent = parent

    def QDSpinBox(
        self, 
        setRange, 
        setSingleStep,
        setValue,
        setMinimumSize,
        setDecimals,
        setAlignment,
                ):
        
        try:
            _QDSpinBox = QDoubleSpinBox(self.parent)
            _QDSpinBox.setRange(*setRange)  # 범위 설정
            _QDSpinBox.setSingleStep(setSingleStep)    # 증가/감소 값 설정
            _QDSpinBox.setValue(setValue)      # 기본값 설정
            _QDSpinBox.setMinimumSize(*setMinimumSize)
            _QDSpinBox.setStyleSheet(QDoubleSpinBoxStyle(self.font_family))
            _QDSpinBox.setDecimals(setDecimals)
            _QDSpinBox.setAlignment(setAlignment)  # 중앙 정렬
            
            return _QDSpinBox
        
        except Exception as e:
            print(f"{self._name} - QDSpinBox Error: ", e)
            return None
        
# 스핀박스 레이블을 구성하는 클래스
class CustomQDSpinBoxLabel:
    def __init__(self, parent):
        self._name = __class__.__name__
        
        # 특정 폴더에 있는 폰트 로드
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        self.parent = parent
    
    def QDSpinBoxLabel(self, LabelText):
        try:
            _QDSBLabel = QLabel(LabelText, self.parent)
            _QDSBLabelType, _QDSBLabelObjID = "QLabel", "QDSBLabel"
            _QDSBLabel.setObjectName(_QDSBLabelObjID)
            _QDSBLabel.setStyleSheet(LabelStyle(_QDSBLabelType+"#"+_QDSBLabelObjID, self.font_family, 16))
            _QDSBLabel.setAlignment(Qt.AlignCenter)
            
            return _QDSBLabel
        
        except Exception as e:
            print(f"{self._name} - QDSpinBoxLabel Error: ", e)
            return None   

