
def LabelStyle(id):
    return """
    %s {
        font-family: arial, helvetica, sans-serif;
        font-size: 25px;
        font-weight: bold;

                            }
                        """ % (id, )

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

                            """ % (id, )
                            


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