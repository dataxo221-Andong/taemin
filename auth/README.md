# HBM Backend Auth API

인증 관련 API 서버 (회원가입, 로그인)

## 🚀 시작하기

### 1. 환경 설정

1. `.env.example` 파일을 복사하여 `.env` 파일 생성
   ```bash
   cp .env.example .env
   ```
   
   Windows (PowerShell):
   ```powershell
   Copy-Item .env.example .env
   ```

2. `.env` 파일에 본인의 데이터베이스 정보 입력
   ```env
   DB_HOST=127.0.0.1
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=project
   DB_CHARSET=utf8mb4
   ```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 서버 실행

```bash
python app.py
```

서버는 `http://0.0.0.0:5000`에서 실행됩니다.

## 📋 API 엔드포인트

### 회원가입
- **URL**: `POST /auth/register`
- **Request Body**:
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```
- **Response**:
  - `201`: 회원가입 성공
  - `400`: 잘못된 요청
  - `409`: 이미 존재하는 사용자

### 로그인
- **URL**: `POST /auth/login`
- **Request Body**:
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```
- **Response**:
  - `200`: 로그인 성공
  - `401`: 비밀번호 불일치
  - `404`: 존재하지 않는 사용자

## 📁 프로젝트 구조 (테이블 준비된 환경 기준)

```
auth/
├── app.py              # Flask 애플리케이션 메인
├── auth_api.py         # 인증 API Blueprint
├── db.py               # 데이터베이스 연결 관리
├── .env.example        # 환경 변수 예시 파일
├── .env                # 환경 변수 파일 (git에 포함 안됨)
├── requirements.txt    # Python 패키지 목록
└── README.md          # 프로젝트 문서
```

## 🔧 환경 변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `DB_HOST` | 데이터베이스 호스트 | `127.0.0.1` |
| `DB_USER` | 데이터베이스 사용자 | `root` |
| `DB_PASSWORD` | 데이터베이스 비밀번호 | (필수) |
| `DB_NAME` | 데이터베이스 이름 | `project` |
| `DB_CHARSET` | 문자 인코딩 | `utf8mb4` |

## 📝 주의사항

- `.env` 파일은 Git에 포함되지 않습니다 (`.gitignore`에 포함)
- 각자 자신의 데이터베이스 정보를 `.env` 파일에 설정해야 합니다

## 🧪 테스트

테스트 파일이 포함되어 있습니다:
- `test_api.py`: 전체 테스트 스위트
- `simple_test.py`: 간단한 테스트

