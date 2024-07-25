import os
from Json_func import *

# 파일 존재 여부 확인 함수
def check_file_exists(file_path):
    # 스크립트 파일의 디렉토리 경로 가져오기
    base_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_path, file_path).replace('\\', '/')

# 폰트 불러오기
def Font_Read(font_path):
    # 특정 폴더 경로
    folder_path = check_file_exists(font_path)
    # 폴더의 파일 목록 가져오기
    files = os.listdir(folder_path)
    
    return files

# 폰트 패치
def Font_path(font_path, access_key):
    Settings = OpenJson(check_file_exists(font_path))
    
    if access_key in Settings.keys():
        return check_file_exists(f"Fonts/Open_Sans/static/{Settings[access_key]}") 
    
    else:
        return check_file_exists("Fonts/Open_Sans/static/OpenSans-Bold.ttf")  # 폰트 파일 경로
