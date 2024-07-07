from PyQt5.QtWidgets import QLabel, QDoubleSpinBox
from PyQt5.QtCore import Qt
from Metal_HUD_parse import *
from GUIStyle import *
from GUIThread import *

class CustomQDoubleSpinBox:
    def __init__(self, parent):
        self.parent = parent

    def QDSpinBox(
        self, 
        setRange, 
        setSingleStep,
        setValue,
        setFixedSize,
        setStyleSheet,
        setDecimals,
        setButtonSymbols,
        setAlignment,
                ):
        
        _QDSpinBox = QDoubleSpinBox(self.parent)
        _QDSpinBox.setRange(*setRange)  # 범위 설정
        _QDSpinBox.setSingleStep(setSingleStep)    # 증가/감소 값 설정
        _QDSpinBox.setValue(setValue)      # 기본값 설정
        _QDSpinBox.setFixedSize(*setFixedSize)
        _QDSpinBox.setStyleSheet(setStyleSheet)
        _QDSpinBox.setDecimals(setDecimals)
        _QDSpinBox.setButtonSymbols(setButtonSymbols)
        _QDSpinBox.setAlignment(setAlignment)  # 중앙 정렬
        
        return _QDSpinBox

class CustomQDSpinBoxLabel:
    def __init__(self, parent):
        self.parent = parent
    
    def QDSpinBoxLabel(self, LabelText, setStyleSheet):
        _QDSBLabel = QLabel(LabelText, self.parent)
        _QDSBLabelType, _QDSBLabelObjID = "QLabel", "QDSBLabel"
        _QDSBLabel.setObjectName(_QDSBLabelObjID)
        _QDSBLabel.setStyleSheet(setStyleSheet(_QDSBLabelType+"#"+_QDSBLabelObjID, 16))
        _QDSBLabel.setAlignment(Qt.AlignCenter)
        
        return _QDSBLabel
        

