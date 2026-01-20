from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db


# Blueprint 생성
# url_prefix="/auth"로 설정되어 있어 모든 라우트는 /auth 접두사를 가집니다
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# 회원가입 API
# POST /auth/register
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        # JSON 데이터 확인
        if not request.json:
            return jsonify({"error": "데이터가 없습니다."}), 400

        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # 필수 필드 검증
        if not username or not password:
            return jsonify({"error": "username과 password 필요"}), 400

        # 입력값 검증 및 공백 제거
        username = username.strip() if isinstance(username, str) else username
        password = password.strip() if isinstance(password, str) else password

        # 공백 제거 후 빈 값 확인
        if not username or not password:
            return jsonify({"error": "username과 password는 빈 값일 수 없습니다."}), 400

        # 비밀번호 해싱
        hashed_pw = generate_password_hash(password)

        # 데이터베이스 연결 가져오기 (db.py에서 pymysql 연결)
        db = get_db()
        if db is None:
            return jsonify({"error": "데이터베이스 연결 실패"}), 500
        
        cur = db.cursor()
        try:
            # 'user' 데이터베이스의 users 테이블에 삽입
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_pw)
            )
            db.commit()
            return jsonify({"message": "회원가입 성공"}), 201
        except Exception as db_error:
            db.rollback()
            # pymysql IntegrityError 체크 (에러 코드 1062는 중복 키)
            if hasattr(db_error, 'args') and len(db_error.args) > 0:
                if db_error.args[0] == 1062 or "Duplicate" in str(db_error):
                    return jsonify({"error": "이미 존재하는 사용자"}), 409
            elif "Duplicate" in str(db_error) or "UNIQUE" in str(db_error):
                return jsonify({"error": "이미 존재하는 사용자"}), 409
            raise
        finally:
            cur.close()

    except Exception as e:
        return jsonify({"error": f"회원가입 실패: {str(e)}"}), 500


# 로그인 API
# POST /auth/login
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        # JSON 데이터 확인
        if not request.json:
            return jsonify({"error": "데이터가 없습니다."}), 400

        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # 필수 필드 검증
        if not username or not password:
            return jsonify({"error": "username과 password 필요"}), 400

        # 입력값 검증 및 공백 제거
        username = username.strip() if isinstance(username, str) else username
        password = password.strip() if isinstance(password, str) else password

        # 공백 제거 후 빈 값 확인
        if not username or not password:
            return jsonify({"error": "username과 password는 빈 값일 수 없습니다."}), 400

        # 데이터베이스 연결 가져오기 (db.py에서 pymysql 연결)
        db = get_db()
        if db is None:
            return jsonify({"error": "데이터베이스 연결 실패"}), 500
        
        cur = db.cursor()
        try:
            # 'user' 데이터베이스의 users 테이블에서 사용자 조회
            cur.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cur.fetchone()

            # 사용자 존재 여부 확인
            if not result:
                return jsonify({"error": "존재하지 않는 사용자"}), 404

            stored_password = result[0]
            
            # 비밀번호가 문자열인지 확인
            if not isinstance(stored_password, str):
                return jsonify({"error": "로그인 실패"}), 500

            # 비밀번호 검증
            if check_password_hash(stored_password, password):
                return jsonify({"message": "로그인 성공"}), 200
            else:
                return jsonify({"error": "비밀번호 틀림"}), 401
        except Exception as db_error:
            return jsonify({"error": f"데이터베이스 오류: {str(db_error)}"}), 500
        finally:
            cur.close()

    except Exception as e:
        return jsonify({"error": f"로그인 실패: {str(e)}"}), 500

