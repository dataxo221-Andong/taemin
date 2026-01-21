-- ============================================
-- 데이터베이스 및 테이블 스키마
-- auth_api.py에 맞는 MySQL 스키마
-- 실행 방법:
--   1. 환경 변수 설정 후: python run_schema.py (권장)
--   2. 직접 실행: mysql -u root -p < schema.sql
-- ============================================

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS my_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 데이터베이스 사용
USE my_db;

-- users 테이블 생성
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '사용자 고유 ID',
    username VARCHAR(100) UNIQUE NOT NULL COMMENT '사용자명 (중복 불가)',
    password VARCHAR(255) NOT NULL COMMENT '해시된 비밀번호',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '생성 일시',
    INDEX idx_username (username) COMMENT 'username 검색 인덱스'
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci
COMMENT='사용자 인증 테이블';

-- 테이블 정보 확인
-- SHOW CREATE TABLE users;
-- DESCRIBE users;

