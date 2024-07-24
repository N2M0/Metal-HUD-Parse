Metal HUD 데이터 처리를 위한 간단한 코드입니다.
pandas, PyQt5, sys 가 필요합니다.

GUI 실행은 MainGUI.py 에서 실행 할 수 있습니다.

GUI 실행시 문제가 발생하면 아이콘 • 설정 파일의 경로 수정이 필요합니다.


```

 ## # Toolbar FilePath
SettingFilePath = r"Metal-HUD-Parse\GUI\Settings\Settings_LBL_CB.json"
ButtonFilePath = r"Metal-HUD-Parse\GUI\Settings\Settings_BTN.json"
SetDataFilePath = r"Metal-HUD-Parse\GUI\Settings\Settings.json"

## # Icon FilePath
DouSBUpIConFilePath = "Metal-HUD-Parse/GUI/icons/up-arrow(DoubleSpinBox).png"
DouSBDownIConFilePath = "Metal-HUD-Parse/GUI/icons/down-arrow(DoubleSpinBox).png"
CBDownIconFilePath = "Metal-HUD-Parse/GUI/icons/down-arrow(ComboBox).png"

 ```


위 경로를 복사해서 constant.py 에서 경로 수정이 필요합니다.
추후에 자동으로 경로를 찾아주는 기능을 추가할 것 입니다.