import sqlite3
from datetime import datetime

DATABASE = 'academy_attendance.db'

def get_db_connection():
    """데이터베이스 연결을 반환합니다."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """데이터베이스를 초기화합니다."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 학생 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 출석 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date DATE NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('출석', '결석', '지각')),
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
            UNIQUE(student_id, date)
        )
    ''')

    conn.commit()
    conn.close()
    print("데이터베이스가 초기화되었습니다.")

if __name__ == '__main__':
    init_db()
