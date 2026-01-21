"""
schema.sql 파일 실행 스크립트
환경 변수를 사용하여 데이터베이스를 초기화합니다.
실행 방법: python run_schema.py
"""
import pymysql
import os
from dotenv import load_dotenv
import re


# .env 파일에서 환경 변수 로드
load_dotenv()


# 데이터베이스 연결 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4')
}

DATABASE_NAME = os.getenv('DB_NAME', 'my_db')


def execute_schema():
    """schema.sql 파일을 읽어서 실행"""
    try:
        # schema.sql 파일 읽기
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        if not os.path.exists(schema_path):
            print(f"✗ schema.sql 파일을 찾을 수 없습니다.")
            return False
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 주석 제거 및 SQL 문 분리
        sql_statements = []
        current_stmt = []
        
        for line in sql_content.split('\n'):
            line = line.strip()
            # 주석 제거
            if line.startswith('--') or not line:
                continue
            # 세미콜론으로 SQL 문 끝 구분
            if ';' in line:
                parts = line.split(';', 1)
                current_stmt.append(parts[0].strip())
                if any(current_stmt):
                    sql_statements.append(' '.join(current_stmt))
                current_stmt = [parts[1].strip()] if parts[1].strip() else []
            else:
                current_stmt.append(line)
        
        # 데이터베이스 연결
        conn = pymysql.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # SQL 문 실행
        for sql in sql_statements:
            if sql.strip():
                try:
                    # 데이터베이스 이름을 환경 변수로 대체
                    sql = sql.replace('my_db', DATABASE_NAME)
                    cur.execute(sql)
                    conn.commit()
                except Exception as e:
                    # USE 문은 에러가 날 수 있으므로 무시
                    if 'USE' not in sql.upper():
                        print(f"⚠ 경고: SQL 실행 중 오류 (무시됨): {str(e)}")
        
        print("✓ schema.sql 실행 완료")
        
        # 테이블 확인
        cur.execute(f"USE {DATABASE_NAME}")
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        print(f"✓ 생성된 테이블: {[table[0] for table in tables]}")
        
        # users 테이블 구조 확인
        cur.execute("DESCRIBE users")
        columns = cur.fetchall()
        print("\n테이블 구조:")
        print("-" * 70)
        for col in columns:
            print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        print("-" * 70)
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ schema.sql 실행 실패: {str(e)}")
        print("\n환경 변수를 확인해주세요:")
        print(f"  DB_HOST: {DB_CONFIG['host']}")
        print(f"  DB_USER: {DB_CONFIG['user']}")
        print(f"  DB_NAME: {DATABASE_NAME}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("데이터베이스 초기화 (schema.sql 실행)")
    print("=" * 70)
    
    if execute_schema():
        print("\n✓ 데이터베이스 초기화 완료!")
        print(f"데이터베이스: {DATABASE_NAME}")
        print("테이블: users")
        print("\n이제 Flask 애플리케이션을 실행할 수 있습니다:")
        print("  python app.py")
    else:
        print("\n✗ 데이터베이스 초기화 실패")
        print("\n확인 사항:")
        print("1. .env 파일이 존재하는지 확인")
        print("2. .env 파일에 올바른 데이터베이스 정보가 있는지 확인")
        print("3. MySQL 서버가 실행 중인지 확인")

