from flask import Flask, render_template, request, jsonify, Response
from database import get_db_connection, init_db
from report_generator import generate_report, save_report
from datetime import datetime
import os

app = Flask(__name__)

# 애플리케이션 시작 시 데이터베이스 초기화
if not os.path.exists('academy_attendance.db'):
    init_db()

@app.route('/')
def index():
    """메인 페이지를 렌더링합니다."""
    return render_template('index.html')

# 학생 관리 API
@app.route('/api/students', methods=['GET'])
def get_students():
    """모든 학생 목록을 조회합니다."""
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])

@app.route('/api/students', methods=['POST'])
def add_student():
    """새로운 학생을 추가합니다."""
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone', '')

    if not name:
        return jsonify({'error': '학생 이름은 필수입니다.'}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO students (name, phone) VALUES (?, ?)',
        (name, phone)
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': student_id, 'message': '학생이 추가되었습니다.'}), 201

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """학생을 삭제합니다."""
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': '학생이 삭제되었습니다.'})

# 출석 관리 API
@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    """출석을 체크합니다."""
    data = request.get_json()
    student_id = data.get('student_id')
    date = data.get('date')
    status = data.get('status')
    note = data.get('note', '')

    if not all([student_id, date, status]):
        return jsonify({'error': '필수 정보가 누락되었습니다.'}), 400

    if status not in ['출석', '결석', '지각']:
        return jsonify({'error': '유효하지 않은 출석 상태입니다.'}), 400

    conn = get_db_connection()
    try:
        # 기존 출석 기록이 있으면 업데이트, 없으면 삽입
        existing = conn.execute(
            'SELECT id FROM attendance WHERE student_id = ? AND date = ?',
            (student_id, date)
        ).fetchone()

        if existing:
            conn.execute(
                'UPDATE attendance SET status = ?, note = ? WHERE student_id = ? AND date = ?',
                (status, note, student_id, date)
            )
        else:
            conn.execute(
                'INSERT INTO attendance (student_id, date, status, note) VALUES (?, ?, ?, ?)',
                (student_id, date, status, note)
            )

        conn.commit()
        conn.close()
        return jsonify({'message': '출석이 기록되었습니다.'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """출석 기록을 조회합니다."""
    date = request.args.get('date')
    student_id = request.args.get('student_id')

    conn = get_db_connection()

    if date and student_id:
        # 특정 학생의 특정 날짜 출석 기록
        attendance = conn.execute('''
            SELECT a.*, s.name as student_name
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE a.date = ? AND a.student_id = ?
        ''', (date, student_id)).fetchall()
    elif date:
        # 특정 날짜의 모든 출석 기록
        attendance = conn.execute('''
            SELECT a.*, s.name as student_name
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE a.date = ?
            ORDER BY s.name
        ''', (date,)).fetchall()
    elif student_id:
        # 특정 학생의 모든 출석 기록
        attendance = conn.execute('''
            SELECT a.*, s.name as student_name
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE a.student_id = ?
            ORDER BY a.date DESC
        ''', (student_id,)).fetchall()
    else:
        # 최근 출석 기록 (최근 30일)
        attendance = conn.execute('''
            SELECT a.*, s.name as student_name
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            ORDER BY a.date DESC, s.name
            LIMIT 100
        ''').fetchall()

    conn.close()

    return jsonify([dict(record) for record in attendance])

@app.route('/api/attendance/stats', methods=['GET'])
def get_attendance_stats():
    """출석 통계를 조회합니다."""
    student_id = request.args.get('student_id')

    conn = get_db_connection()

    if student_id:
        # 특정 학생의 출석 통계
        stats = conn.execute('''
            SELECT
                status,
                COUNT(*) as count
            FROM attendance
            WHERE student_id = ?
            GROUP BY status
        ''', (student_id,)).fetchall()
    else:
        # 전체 출석 통계
        stats = conn.execute('''
            SELECT
                status,
                COUNT(*) as count
            FROM attendance
            GROUP BY status
        ''').fetchall()

    conn.close()

    return jsonify([dict(stat) for stat in stats])

# Daily Study Report API
@app.route('/api/report', methods=['POST'])
def create_report():
    """Daily Study Report를 생성합니다."""
    data = request.get_json()

    # 필수 필드 검증
    name = data.get('name')
    textbook = data.get('textbook')
    progress = data.get('progress')

    if not all([name, textbook, progress]):
        return jsonify({'error': '학생 이름, 교재, 진도는 필수 항목입니다.'}), 400

    # 보고서 데이터 구성
    report_data = {
        'name': name,
        'textbook': textbook,
        'progress': progress,
        'homework': data.get('homework', ''),
        'vocabulary': data.get('vocabulary', ''),
        'reading': data.get('reading', ''),
        'expression': data.get('expression', ''),
        'grammar': data.get('grammar', ''),
        'test': data.get('test', ''),
        'notes': data.get('notes', '')
    }

    try:
        # 보고서 생성
        report_text = generate_report(report_data)
        return jsonify({
            'success': True,
            'report': report_text,
            'message': '보고서가 성공적으로 생성되었습니다.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/report/download', methods=['POST'])
def download_report():
    """생성된 보고서를 텍스트 파일로 다운로드합니다."""
    data = request.get_json()
    report_text = data.get('report', '')
    student_name = data.get('name', 'student')

    if not report_text:
        return jsonify({'error': '보고서 내용이 없습니다.'}), 400

    # 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"daily_report_{student_name}_{timestamp}.txt"

    # 텍스트 파일로 응답
    return Response(
        report_text,
        mimetype='text/plain',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


@app.route('/report')
def report_page():
    """Daily Study Report 작성 페이지를 렌더링합니다."""
    return render_template('report.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
