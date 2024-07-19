from PyQt5.QtWidgets import QLabel, QDoubleSpinBox
from PyQt5.QtCore import Qt
from Metal_HUD_parse import *
from GUIStyle import *

# 스핀박스를 구성하는 클래스
class CustomQDoubleSpinBox:
    def __init__(self, parent):
        self.parent = parent

    def QDSpinBox(
        self, 
        setRange, 
        setSingleStep,
        setValue,
        setMinimumSize,
        setStyleSheet,
        setDecimals,
        setAlignment,
                ):
        
        try:
            _QDSpinBox = QDoubleSpinBox(self.parent)
            _QDSpinBox.setRange(*setRange)  # 범위 설정
            _QDSpinBox.setSingleStep(setSingleStep)    # 증가/감소 값 설정
            _QDSpinBox.setValue(setValue)      # 기본값 설정
            _QDSpinBox.setMinimumSize(*setMinimumSize)
            _QDSpinBox.setStyleSheet(setStyleSheet)
            _QDSpinBox.setDecimals(setDecimals)
            _QDSpinBox.setAlignment(setAlignment)  # 중앙 정렬
            
            return _QDSpinBox
        
        except Exception as e:
            print("QDSpinBox Error: ", e)
            return None
        
# 스핀박스 레이블을 구성하는 클래스
class CustomQDSpinBoxLabel:
    def __init__(self, parent):
        self.parent = parent
    
    def QDSpinBoxLabel(self, LabelText, setStyleSheet):
        try:
            _QDSBLabel = QLabel(LabelText, self.parent)
            _QDSBLabelType, _QDSBLabelObjID = "QLabel", "QDSBLabel"
            _QDSBLabel.setObjectName(_QDSBLabelObjID)
            _QDSBLabel.setStyleSheet(setStyleSheet(_QDSBLabelType+"#"+_QDSBLabelObjID, 16))
            _QDSBLabel.setAlignment(Qt.AlignCenter)
            
            return _QDSBLabel
        
        except Exception as e:
            print("CustomQDSpinBoxLabel Error: ", e)
            return None   

