import os
from Json_Utils import *
from datetime import datetime

# 여기는 config_paths 에서 주로 사용되는 보조 함수를 관리하는 파일입니다.
# config_paths 가 아닌 파일에서도 사용됩니다.

# 주어진 파일 경로에 대한 절대 경로를 반환하는 함수
def get_absolute_path(relative_path):
    # 현재 스크립트 파일의 디렉토리 경로 가져오기
    base_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_path, relative_path).replace('\\', '/')

# 폰트 불러오기
def Font_Read(font_path):
    # 적용되지 않는 폰트들
    remove_font = [
        "OpenSans_SemiCondensed-SemiBoldItalic.ttf", 
        "OpenSans_SemiCondensed-SemiBold.ttf", 
        "OpenSans_SemiCondensed-ExtraBold.ttf", 
        "OpenSans_SemiCondensed-ExtraBoldItalic.ttf"
        ]
    
    # 특정 폴더 경로 확인 및 파일 목록 가져오기
    folder_path = get_absolute_path(font_path)
    
    # 파일 목록 필터링
    filtered_files = [
        file for file in os.listdir(folder_path) 
        if file not in remove_font
        ]
    
    return filtered_files

# 폰트 패치
def Font_Path(font_path, access_key):
    Settings = OpenJson(get_absolute_path(font_path))
    
    if access_key in Settings.keys():
        return get_absolute_path(f"Fonts/Open_Sans/static/{Settings[access_key]}") 
    
    else:
        return get_absolute_path("Fonts/Open_Sans/static/OpenSans-Bold.ttf")  # 폰트 파일 경로

# 현재시간
def CurrentTime():
    dt = datetime.now()
    
    # AM = 오전
    meridiem = "AM" if dt.hour < 12 else "PM" 
    
    # 12형식
    dt_hour = dt.hour % 12
    hour = 12 if dt_hour == 0 else dt_hour
    
    return dt.strftime(f"%Y-%m-%d_{meridiem}_{hour}-%M-%S")

# 폴더 생성
def MakeFolder(folder_name):
    if folder_name is not None:
        folder_path = get_absolute_path(folder_name)
        
        # 디렉토리가 존재하는지 확인
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # 디렉토리가 없으면 생성
            return folder_path  # 새로 생성한 폴더 경로 반환
        else:
            return folder_path  # 이미 존재하는 경우 기존 경로 반환
    else:
        raise ValueError("folder_name은 None이 될 수 없습니다.")