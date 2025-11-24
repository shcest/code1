# 학원 출석부 시스템

학원에서 학생들의 출석을 관리할 수 있는 웹 애플리케이션입니다.

## 주요 기능

- **학생 관리**: 학생 추가, 조회, 삭제
- **출석 체크**: 날짜별 출석, 결석, 지각 기록
- **출석 조회**: 일별, 학생별 출석 기록 조회
- **통계**: 전체 출석 통계 확인
- **반응형 디자인**: 모바일, 태블릿, 데스크톱 지원

## 기술 스택

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **스타일**: 그라데이션 기반 모던 UI

## 설치 방법

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 초기화

```bash
python database.py
```

### 3. 애플리케이션 실행

```bash
python app.py
```

### 4. 브라우저에서 접속

```
http://localhost:5000
```

## 사용 방법

### 학생 추가
1. "학생 관리" 섹션에서 학생 이름과 전화번호를 입력
2. "학생 추가" 버튼 클릭

### 출석 체크
1. "출석 체크" 섹션에서 날짜 선택
2. 학생 선택
3. 출석 상태 선택 (출석/결석/지각)
4. 필요시 메모 입력
5. "출석 체크" 버튼 클릭

### 출석 현황 조회
- "오늘 출석 현황" 버튼: 오늘 날짜의 출석 기록 보기
- "전체 출석 기록" 버튼: 최근 출석 기록 보기

## 프로젝트 구조

```
.
├── app.py              # Flask 애플리케이션 메인 파일
├── database.py         # 데이터베이스 초기화 및 관리
├── requirements.txt    # Python 패키지 의존성
├── static/
│   ├── style.css      # CSS 스타일시트
│   └── script.js      # JavaScript 클라이언트 코드
└── templates/
    └── index.html     # HTML 템플릿
```

## API 엔드포인트

### 학생 관리
- `GET /api/students` - 모든 학생 조회
- `POST /api/students` - 새 학생 추가
- `DELETE /api/students/<id>` - 학생 삭제

### 출석 관리
- `POST /api/attendance` - 출석 기록 추가/수정
- `GET /api/attendance` - 출석 기록 조회
  - 쿼리 파라미터: `date`, `student_id`
- `GET /api/attendance/stats` - 출석 통계 조회

## 데이터베이스 스키마

### students 테이블
- `id`: 학생 ID (기본키)
- `name`: 학생 이름
- `phone`: 전화번호
- `created_at`: 등록일시

### attendance 테이블
- `id`: 출석 기록 ID (기본키)
- `student_id`: 학생 ID (외래키)
- `date`: 출석 날짜
- `status`: 출석 상태 (출석/결석/지각)
- `note`: 메모
- `created_at`: 기록일시

## 라이선스

MIT License
