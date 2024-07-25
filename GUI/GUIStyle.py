from constant import *
from PyQt5 import QtGui


def LabelStyle(id, font_family, fontsize, color="black"):
    return """
    %s {
        font-family: '%s';
        font-size: %spx;
        color: %s

                            }
                        """ % (id, font_family, fontsize, color)

def ButtonStyle(id, font_family):
    return """
        %s {
            font-family: '%s';
            font-size: 25px;
            color: white;
            background-color: rgb(58, 134, 255);
            border-radius: 15px;

                            }
        
        %s:hover {
                background-color: #e0e0e0;
            }

        %s:pressed {
                background-color: #d0d0d0;
            }

                            """ % (id, font_family, id, id)



# 저작권 표시
# 1. up-button 
# 1. <a href="https://www.flaticon.com/free-icons/up-arrow" title="up arrow icons">Up arrow icons created by Roundicons - Flaticon</a>
# 2. down-button
# 2. <a href="https://www.flaticon.com/free-icons/down-arrow" title="down arrow icons">Down arrow icons created by Roundicons - Flaticon</a>
def QDoubleSpinBoxStyle(font_family):
    return """
        QDoubleSpinBox {
            font-family: '%s';
            font-size: 18px;
            color: black;
            background-color: #f0f0f0;
            border: 1px solid #a0a0a0;
            border-radius: 10px;
            padding: 2px;
        }

        QDoubleSpinBox::up-button {
            image: url(%s);
            width: 20px;
            height: 20px;;
            subcontrol-origin: padding;
            subcontrol-position: top right;
            margin-right: 5px;
            margin-top: 4px;
        }

        QDoubleSpinBox::down-button {
            image: url(%s);
            width: 20px;;
            height: 20px;;
            subcontrol-origin: padding;
            subcontrol-position: bottom right;
            margin-right: 5px;
            margin-bottom: 4px;
        }
            
            """ % (
                font_family,
                DouSBUpIConFilePath,
                DouSBDownIConFilePath,
            )

def MsgBoxStyle(font_family):
    return """
            QMessageBox {
                font-family: '%s';
                font-size: 15px;
                border-radius: 15px;
            }
            QPushButton {
                font-family: '%s';
                font-size: 15px;
                background-color: rgb(58, 134, 255);
                border-radius: 15px;
                color: white;
                width: 70px;
                height: 35px;
            }
                
            QLabel{
                min-width: 300px;
                }
        """ % (font_family, font_family)



def ToolbarStyle(font_family):
    return """
            QToolBar {
                background-color: #f0f0f0;
                border: none;
                margin: 0px;
            }

            QToolButton {
                font-family: '%s';
                background-color: transparent;
                border: none;
                padding: 8px;
                border-radius: 8px;  /* Inherit toolbar's rounded corners */
                color: white;
                background-color: rgb(58, 134, 255);
            }

            QToolButton:hover {
                background-color: #e0e0e0;
            }

            QToolButton:pressed {
                background-color: #d0d0d0;
            }
        """ % font_family



def PbarStyle(font_family):
    return """
            QProgressBar {
                font-family: '%s';
                border: 2px solid grey;
                border-radius: 8px;
                background-color: #FFFFFF;
    
            }

            QProgressBar::chunk {
                background-color: rgb(58, 134, 255);
                border-radius: 5px; /* 둥근 효과 */
            }
        """ % font_family


# 저작권 표시
# 1. QComboBox::down-arrow
# 1. <a href="https://www.flaticon.com/free-icons/down-arrow" title="down arrow icons">Down arrow icons created by Roundicons - Flaticon</a>
def ComboBoxStyle(font_family):
    return """
        QComboBox {
            font-family: '%s';
            font-size: 15px;
            border-radius: 4px;
            border: 2px solid rgb(58, 134, 255);;
            padding: 3px;
            background-color: white;
            margin: 1px;

        }

        QComboBox:focus, QComboBox:on {
            border-radius: 4px;
            border: 4px solid rgb(58, 134, 255);
            margin:0px;
        }

        QComboBox::drop-down {
            border:none;
        }
        
        QComboBox::down-arrow {
            image: url(%s);
            width: 15px;
            height: 15px;
            margin-right: 10px;
        }
        
        QComboBox QAbstractItemView {
            border: 1px solid rgb(175, 175, 175);
            font-family: '%s';
            font-size: 15px;
        }

    """ % (font_family, CBDownIconFilePath, font_family)

