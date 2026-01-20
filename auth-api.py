from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
DB_NAME = "users.db"


# --------------------
# DB 초기화
# --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# --------------------
# 회원가입
# --------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        if not request.json:
            return jsonify({"error": "데이터가 없습니다."}), 400

        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "username과 password 필요"}), 400

        # 입력값 검증
        username = username.strip() if isinstance(username, str) else username
        password = password.strip() if isinstance(password, str) else password

        if not username or not password:
            return jsonify({"error": "username과 password는 빈 값일 수 없습니다."}), 400

        hashed_pw = generate_password_hash(password)

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_pw)
            )
            conn.commit()
            return jsonify({"message": "회원가입 성공"}), 201
        except sqlite3.IntegrityError:
            conn.rollback()
            return jsonify({"error": "이미 존재하는 사용자"}), 409
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"error": f"회원가입 실패: {str(e)}"}), 500


# --------------------
# 로그인
# --------------------
@app.route("/login", methods=["POST"])
def login():
    try:
        if not request.json:
            return jsonify({"error": "데이터가 없습니다."}), 400

        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "username과 password 필요"}), 400

        # 입력값 검증 및 공백 제거
        username = username.strip() if isinstance(username, str) else username
        password = password.strip() if isinstance(password, str) else password

        if not username or not password:
            return jsonify({"error": "username과 password는 빈 값일 수 없습니다."}), 400

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        try:
            cur.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cur.fetchone()

            if not result:
                return jsonify({"error": "존재하지 않는 사용자"}), 404

            stored_password = result[0]

            if check_password_hash(stored_password, password):
                return jsonify({"message": "로그인 성공"}), 200
            else:
                return jsonify({"error": "비밀번호 틀림"}), 401
        finally:
            conn.close()

    except Exception as e:
        return jsonify({"error": f"로그인 실패: {str(e)}"}), 500


# --------------------
# 실행
# --------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
