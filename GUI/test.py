from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget

app = QApplication([])

# 콤보박스 생성
combobox = QComboBox()

# 콤보박스 스타일 설정
combobox.setStyleSheet("""
    QComboBox::drop-down {
            border:none;
        }

    QComboBox::down-arrow {
        image: url(GUI/icons/free-icon-down-arrow-271210.png);
        width: 16px;
        height: 16px;
        margin-right: 10px;
    }
""")

# 레이아웃 생성 및 콤보박스 추가
layout = QVBoxLayout()
layout.addWidget(combobox)

window = QWidget()
window.setLayout(layout)
window.show()

app.exec_()
