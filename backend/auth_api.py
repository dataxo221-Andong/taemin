from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
import pymysql

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# --------------------
# 공통 유틸 함수
# --------------------
def get_json_data():
    if not request.is_json:
        return None, jsonify({"error": "JSON 데이터가 없습니다."}), 400
    data = request.get_json()
    if data is None:
        return None, jsonify({"error": "JSON 데이터가 없습니다."}), 400
    return data, None, None


def validate_user_input(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return None, None, jsonify({"error": "username과 password 필요"}), 400

    # 문자열 타입 확인
    if not isinstance(username, str) or not isinstance(password, str):
        return None, None, jsonify({"error": "username과 password는 문자열이어야 합니다."}), 400

    username = username.strip()
    password = password.strip()

    if not username or not password:
        return None, None, jsonify({"error": "username과 password는 빈 값일 수 없습니다."}), 400

    return username, password, None, None


# --------------------
# 회원가입
# --------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data, error_res, status = get_json_data()
    if error_res:
        return error_res, status

    username, password, error_res, status = validate_user_input(data)
    if error_res:
        return error_res, status

    hashed_pw = generate_password_hash(password)

    conn = get_db()
    if conn is None:
        return jsonify({"error": "데이터베이스 연결 실패"}), 500

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_pw)
        )
        conn.commit()
        return jsonify({"message": "회원가입 성공"}), 201

    except (pymysql.err.IntegrityError, pymysql.IntegrityError) as e:
        conn.rollback()
        # 에러 코드 1062는 중복 키 에러
        if hasattr(e, 'args') and len(e.args) > 0 and e.args[0] == 1062:
            return jsonify({"error": "이미 존재하는 사용자"}), 409
        return jsonify({"error": "이미 존재하는 사용자"}), 409

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"회원가입 실패: {str(e)}"}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# --------------------
# 로그인
# --------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data, error_res, status = get_json_data()
    if error_res:
        return error_res, status

    username, password, error_res, status = validate_user_input(data)
    if error_res:
        return error_res, status

    conn = get_db()
    if conn is None:
        return jsonify({"error": "데이터베이스 연결 실패"}), 500

    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT password FROM users WHERE username = %s",
            (username,)
        )
        result = cur.fetchone()

        if not result:
            return jsonify({"error": "존재하지 않는 사용자"}), 404

        stored_pw = result["password"] if isinstance(result, dict) else result[0]

        if check_password_hash(stored_pw, password):
            return jsonify({"message": "로그인 성공"}), 200
        else:
            return jsonify({"error": "비밀번호 틀림"}), 401

    except Exception as e:
        return jsonify({"error": f"로그인 실패: {str(e)}"}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
