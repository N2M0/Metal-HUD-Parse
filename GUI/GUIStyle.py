
def LabelStyle(id, fontsize):
    return """
    %s {
        font-family: arial, helvetica, sans-serif;
        font-size: %spx;
        font-weight: bold;

                            }
                        """ % (id, fontsize)

def ButtonStyle(id):
    return """
        %s {
            font-family: arial, helvetica, sans-serif;
            font-size: 25px;
            font-weight: bold;
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

                            """ % (id, id, id)



# 저작권 표시
# 1. up-button 
# 1. <a href="https://www.flaticon.com/free-icons/up-arrow" title="up arrow icons">Up arrow icons created by Roundicons - Flaticon</a>
# 2. down-button
# 2. <a href="https://www.flaticon.com/free-icons/down-arrow" title="down arrow icons">Down arrow icons created by Roundicons - Flaticon</a>
def QDoubleSpinBoxStyle():
    return """
        QDoubleSpinBox {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: black;
            background-color: #f0f0f0;
            border: 1px solid #a0a0a0;
            border-radius: 10px;
            padding: 2px;
        }

        QDoubleSpinBox::up-button {
            image: url(GUI/icons/up-arrow(DoubleSpinBox).png);
            width: 20px;
            height: 20px;;
            subcontrol-origin: padding;
            subcontrol-position: top right;
            margin-right: 5px;
            margin-top: 5px;
        }

        QDoubleSpinBox::down-button {
            image: url(GUI/icons/down-arrow(DoubleSpinBox).png);
            width: 20px;;
            height: 20px;;
            subcontrol-origin: padding;
            subcontrol-position: bottom right;
            margin-right: 5px;
            margin-bottom: 5px;
        }
            
            """

def MsgBoxStyle():
    return """
            QMessageBox {
                font-family: arial, helvetica, sans-serif;
                font-size: 15px;
                font-weight: bold;
                border-radius: 15px;
            }
            QPushButton {
                font-family: arial, helvetica, sans-serif;
                font-size: 15px;
                font-weight: bold;
                background-color: rgb(58, 134, 255);
                border-radius: 15px;
                color: white;
                width: 70px;
                height: 35px;
            }
                
            QLabel{
                min-width: 400px;
                }
        """



def ToolbarStyle():
    return """
            QToolBar {
                background-color: #f0f0f0;
                border: none;
                margin: 0px;
            }

            QToolButton {
                font-family: Arial, Helvetica, sans-serif;
                background-color: transparent;
                border: none;
                padding: 8px;
                border-radius: 8px;  /* Inherit toolbar's rounded corners */
                color: white;
                background-color: rgb(58, 134, 255);
                font-weight: bold;
            }

            QToolButton:hover {
                background-color: #e0e0e0;
            }

            QToolButton:pressed {
                background-color: #d0d0d0;
            }
        """



def PbarStyle():
    return """
            QProgressBar {
                font-family: arial, helvetica, sans-serif;
                font-weight: bold;
                border: 2px solid grey;
                border-radius: 8px;
                background-color: #FFFFFF;
    
            }

            QProgressBar::chunk {
                background-color: rgb(58, 134, 255);
                border-radius: 5px; /* 둥근 효과 */
            }
        """


# 저작권 표시
# 1. QComboBox::down-arrow
# 1. <a href="https://www.flaticon.com/free-icons/down-arrow" title="down arrow icons">Down arrow icons created by Roundicons - Flaticon</a>
def ComboBoxStyle():
    return """
        QComboBox {
            font-family: arial, helvetica, sans-serif;
            font-size: 15px;
            font-weight: bold;
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
            image: url(GUI/icons/down-arrow(ComboBox).png);
            width: 15px;
            height: 15px;
            margin-right: 10px;
        }
        
        QComboBox QAbstractItemView {
            border: 1px solid rgb(175, 175, 175);
            font-family: arial, helvetica, sans-serif;
            font-size: 15px;
            font-weight: bold;
        }

    """
