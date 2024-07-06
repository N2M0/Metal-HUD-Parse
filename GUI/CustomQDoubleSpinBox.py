import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGridLayout, QFrame, QSpacerItem, QSizePolicy, QDoubleSpinBox, QAbstractSpinBox
from PyQt5.QtCore import Qt, QTimer
from Metal_HUD_parse import *
from gui_style import *
from gui_thread import *

class CustomQDoubleSpinBox:
    def __init__(self, parent):
        self.parent = parent

    def QDSpinBox(
        self, 
        setRnage, 
        setSingleStep,
        setValue,
        setFixedSize,
        setStyleSheet,
        setDecimals,
        setButtonSymbols,
        setAlignment,
                ):
        
        
        self._QDSpinBox = QDoubleSpinBox(self.parent)
        self._QDSpinBox.setRange(*setRnage)  # 범위 설정
        self._QDSpinBox.setSingleStep(setSingleStep)    # 증가/감소 값 설정
        self._QDSpinBox.setValue(setValue)      # 기본값 설정
        self._QDSpinBox.setFixedSize(*setFixedSize)
        self._QDSpinBox.setStyleSheet(setStyleSheet)
        self._QDSpinBox.setDecimals(setDecimals)
        self._QDSpinBox.setButtonSymbols(setButtonSymbols)
        self._QDSpinBox.setAlignment(setAlignment)  # 중앙 정렬
        
        return self._QDSpinBox