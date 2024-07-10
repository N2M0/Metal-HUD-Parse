
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

        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
            width: 0px; 
            height: 0px; 
            border: none; /* 버튼의 경계선 제거 */
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
                border: 2px solid grey;
                border-radius: 8px;
                background-color: #FFFFFF;
                font-weight: bold;
    
            }

            QProgressBar::chunk {
                background-color: rgb(58, 134, 255);
                border-radius: 5px; /* 둥근 효과 */
            }
        """