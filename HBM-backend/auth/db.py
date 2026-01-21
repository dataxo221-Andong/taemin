"""
데이터베이스 연결 관리 모듈
환경 변수를 통해 데이터베이스 연결 정보를 관리합니다.
"""
import pymysql
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()


def get_conn():
    """
    데이터베이스 연결을 반환하는 함수
    환경 변수에서 연결 정보를 가져옵니다.
    """
    return pymysql.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'my_db'),
        charset=os.getenv('DB_CHARSET', 'utf8mb4'),
        cursorclass=pymysql.cursors.DictCursor
    )


# auth_api.py와의 호환성을 위해
def get_db():
    """get_conn의 별칭 (auth_api.py에서 사용)"""
    return get_conn()
