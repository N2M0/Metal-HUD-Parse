import logging
from constant import *

def InitLogger():
    # 로거 생성
    logger = logging.getLogger()
    
    # 로거가 이미 설정되어 있으면 추가 설정을 하지 않음
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # 기본 로그 레벨 설정

        # 파일 핸들러 설정
        file_handler = logging.FileHandler(loggingFilePath, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # 파일에 기록할 로그 레벨 설정

        # 스트림 핸들러(터미널) 설정
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)  # 터미널에 출력할 로그 레벨 설정

        # 포맷터 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # 핸들러를 로거에 추가
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    return logger