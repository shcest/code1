// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    // 오늘 날짜 설정
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('attendanceDate').value = today;

    // 데이터 로드
    loadStudents();
    loadAttendanceStats();
});

// 메시지 표시 함수
function showMessage(text, isError = false) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = 'message show';
    if (isError) {
        messageDiv.classList.add('error');
    }

    setTimeout(() => {
        messageDiv.classList.remove('show');
    }, 3000);
}

// 학생 목록 로드
async function loadStudents() {
    try {
        const response = await fetch('/api/students');
        const students = await response.json();

        const studentsDiv = document.getElementById('students');
        const studentSelect = document.getElementById('studentSelect');

        // 학생 목록 표시
        studentsDiv.innerHTML = students.map(student => `
            <div class="student-item">
                <div class="student-info">
                    <div class="student-name">${student.name}</div>
                    ${student.phone ? `<div class="student-phone">📞 ${student.phone}</div>` : ''}
                </div>
                <button class="delete-btn" onclick="deleteStudent(${student.id})">삭제</button>
            </div>
        `).join('');

        // 학생 선택 드롭다운 업데이트
        studentSelect.innerHTML = '<option value="">학생 선택</option>' +
            students.map(student => `
                <option value="${student.id}">${student.name}</option>
            `).join('');

    } catch (error) {
        showMessage('학생 목록을 불러오는데 실패했습니다.', true);
        console.error('Error:', error);
    }
}

// 학생 추가
async function addStudent() {
    const name = document.getElementById('studentName').value.trim();
    const phone = document.getElementById('studentPhone').value.trim();

    if (!name) {
        showMessage('학생 이름을 입력해주세요.', true);
        return;
    }

    try {
        const response = await fetch('/api/students', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, phone })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('학생이 추가되었습니다.');
            document.getElementById('studentName').value = '';
            document.getElementById('studentPhone').value = '';
            loadStudents();
        } else {
            showMessage(data.error || '학생 추가에 실패했습니다.', true);
        }
    } catch (error) {
        showMessage('학생 추가에 실패했습니다.', true);
        console.error('Error:', error);
    }
}

// 학생 삭제
async function deleteStudent(studentId) {
    if (!confirm('정말로 이 학생을 삭제하시겠습니까?')) {
        return;
    }

    try {
        const response = await fetch(`/api/students/${studentId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showMessage('학생이 삭제되었습니다.');
            loadStudents();
            loadAttendanceStats();
        } else {
            showMessage('학생 삭제에 실패했습니다.', true);
        }
    } catch (error) {
        showMessage('학생 삭제에 실패했습니다.', true);
        console.error('Error:', error);
    }
}

// 출석 체크
async function markAttendance() {
    const studentId = document.getElementById('studentSelect').value;
    const date = document.getElementById('attendanceDate').value;
    const status = document.getElementById('attendanceStatus').value;
    const note = document.getElementById('attendanceNote').value.trim();

    if (!studentId) {
        showMessage('학생을 선택해주세요.', true);
        return;
    }

    if (!date) {
        showMessage('날짜를 선택해주세요.', true);
        return;
    }

    try {
        const response = await fetch('/api/attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_id: studentId,
                date: date,
                status: status,
                note: note
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('출석이 기록되었습니다.');
            document.getElementById('attendanceNote').value = '';
            loadAttendanceStats();

            // 오늘 날짜면 오늘 출석 현황 자동 새로고침
            const today = new Date().toISOString().split('T')[0];
            if (date === today) {
                showTodayAttendance();
            }
        } else {
            showMessage(data.error || '출석 체크에 실패했습니다.', true);
        }
    } catch (error) {
        showMessage('출석 체크에 실패했습니다.', true);
        console.error('Error:', error);
    }
}

// 오늘 출석 현황
async function showTodayAttendance() {
    const today = new Date().toISOString().split('T')[0];
    await loadAttendanceRecords(`?date=${today}`);
}

// 전체 출석 기록
async function showAllAttendance() {
    await loadAttendanceRecords('');
}

// 출석 기록 로드
async function loadAttendanceRecords(query = '') {
    try {
        const response = await fetch(`/api/attendance${query}`);
        const records = await response.json();

        const recordsDiv = document.getElementById('attendanceRecords');

        if (records.length === 0) {
            recordsDiv.innerHTML = '<p style="text-align: center; color: #999;">출석 기록이 없습니다.</p>';
            return;
        }

        recordsDiv.innerHTML = records.map(record => `
            <div class="attendance-item">
                <div class="attendance-info">
                    <div class="attendance-student">${record.student_name}</div>
                    <div class="attendance-date">📅 ${record.date}</div>
                    <div class="status-${record.status}">${record.status}</div>
                    ${record.note ? `<div class="attendance-note">📝 ${record.note}</div>` : ''}
                </div>
            </div>
        `).join('');

    } catch (error) {
        showMessage('출석 기록을 불러오는데 실패했습니다.', true);
        console.error('Error:', error);
    }
}

// 출석 통계 로드
async function loadAttendanceStats() {
    try {
        const response = await fetch('/api/attendance/stats');
        const stats = await response.json();

        const statsDiv = document.getElementById('attendanceStats');

        if (stats.length === 0) {
            statsDiv.innerHTML = '<p style="text-align: center; color: #999;">통계 데이터가 없습니다.</p>';
            return;
        }

        statsDiv.innerHTML = stats.map(stat => `
            <div class="stat-card">
                <div class="stat-label">${stat.status}</div>
                <div class="stat-value">${stat.count}</div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error:', error);
    }
}
