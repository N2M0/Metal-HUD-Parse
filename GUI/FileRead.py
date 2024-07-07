import sys
from PyQt5.QtWidgets import  QFileDialog
from PyQt5.QtCore import QTimer
from Metal_HUD_parse import *
from gui_style import *
from gui_thread import *

class FileReader:
    def __init__(self, parent):
        self.parent = parent
        self.FileLabel = parent.FileLabel
        self.FileReadframe = parent.FileReadframe
        self.Mainvbox = parent.Mainvbox
        self.StartPerformanceWindow = parent.StartPerformanceWindow

    def FileRead(self):
        options = QFileDialog.Options()
        FileName, _ = QFileDialog.getOpenFileName(self.parent, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if FileName:
            self.FileLabel.setText(f'Selected File: {FileName}')
            QTimer.singleShot(1000, self.FileReadframe.hide)
            QTimer.singleShot(1000, lambda: self.Mainvbox.addWidget(self.StartPerformanceWindow(FileName)))
            
        else:
            self.FileLabel.setText(f'Selected File: Failed.')

    
    def FileChanged(self):
        options = QFileDialog.Options()
        newFileName, _ = QFileDialog.getOpenFileName(self.parent, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if newFileName:
            return newFileName