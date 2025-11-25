"""
Daily Study Report 자동 생성 모듈
한국 초등부 영어학원 학부모용 학습 피드백 보고서 생성
"""

import random
from datetime import datetime


def get_grade_evaluation(grade):
    """등급에 따른 평가 반환"""
    if grade in ['A', 'A+', '100', '95', '90']:
        return '우수'
    elif grade in ['B', 'B+', '85', '80', '75']:
        return '보통'
    else:
        return '미흡'


def get_grade_level(grade):
    """등급을 표준화된 레벨로 변환"""
    grade_mapping = {
        'A+': 'A+', 'A': 'A', 'B+': 'B+', 'B': 'B', 'C+': 'C+', 'C': 'C', 'D': 'D', 'F': 'F',
        '100': 'A+', '95': 'A', '90': 'A', '85': 'B+', '80': 'B', '75': 'B',
        '70': 'C+', '65': 'C', '60': 'C', '55': 'D', '50': 'D'
    }
    return grade_mapping.get(str(grade), grade)


# 칭찬 문구 템플릿 (다양한 표현)
PRAISE_TEMPLATES = {
    'excellent': [
        "{name} 학생이 오늘 수업에서 정말 열심히 참여하는 모습이 인상적이었습니다.",
        "수업 시간 내내 집중력을 잃지 않고 적극적으로 학습에 임하였습니다.",
        "선생님의 질문에 자신감 있게 대답하는 모습에서 큰 성장을 느꼈습니다.",
        "어려운 문제도 포기하지 않고 끝까지 도전하는 자세가 훌륭했습니다.",
        "영어 학습에 대한 흥미와 열정이 느껴져 매우 기뻤습니다.",
        "배운 내용을 빠르게 이해하고 응용하는 능력이 뛰어납니다.",
        "발음과 억양이 점점 자연스러워지고 있어 앞으로가 더 기대됩니다.",
        "단어 암기력이 우수하여 새로운 어휘를 빠르게 습득하고 있습니다.",
        "문장 구조를 정확히 파악하고 올바르게 활용하는 모습이 대견했습니다.",
        "틀린 문제를 스스로 분석하고 수정하려는 태도가 매우 바람직합니다."
    ],
    'good': [
        "{name} 학생이 오늘 수업에 성실하게 참여하였습니다.",
        "꾸준히 노력하는 모습이 보여 앞으로의 성장이 기대됩니다.",
        "수업 내용을 이해하려고 집중하는 자세가 좋았습니다.",
        "질문에 대답하려고 노력하는 모습이 인상적이었습니다.",
        "조금씩이지만 꾸준한 발전을 보이고 있습니다.",
        "새로운 내용을 배우는 것에 두려움 없이 도전하는 자세가 좋습니다.",
        "친구들과 협력하여 학습하는 모습이 보기 좋았습니다.",
        "오늘 배운 내용을 이해하려고 여러 번 연습하는 끈기가 있습니다.",
        "실수를 두려워하지 않고 영어로 말하려고 시도하는 용기가 대단합니다.",
        "수업 시간에 바른 자세로 앉아 학습에 임하는 모습이 좋았습니다."
    ],
    'needs_improvement': [
        "{name} 학생이 오늘 수업에서 최선을 다해 참여하였습니다.",
        "어려운 내용에도 포기하지 않고 끝까지 함께 해주어 고마웠습니다.",
        "조금 힘들어하는 모습이 보였지만, 그래도 끝까지 수업에 집중해 주었습니다.",
        "새로운 개념을 이해하는 데 시간이 걸리지만 차분히 배워가고 있습니다.",
        "아직 익숙하지 않은 부분이 있지만 점점 나아지고 있습니다.",
        "선생님과 함께 차근차근 연습하며 조금씩 발전하고 있습니다.",
        "처음에는 어려워했지만 반복 학습을 통해 이해도가 높아지고 있습니다.",
        "학습 의지를 잃지 않고 꾸준히 노력하는 모습이 보입니다.",
        "어려운 문제를 만나도 도움을 요청할 줄 아는 지혜가 있습니다.",
        "오늘 배운 내용을 복습하면 더 빠르게 성장할 수 있을 것입니다."
    ]
}

# 개선점 문구 템플릿
IMPROVEMENT_TEMPLATES = {
    'vocabulary': [
        "단어 암기에서 조금 어려움을 겪었는데, 매일 조금씩 반복하면 충분히 극복할 수 있습니다.",
        "새로운 어휘를 외우는 데 시간이 더 필요해 보입니다. 학원에서 추가 복습 시간을 마련하겠습니다.",
        "단어의 철자와 의미를 연결짓는 연습이 더 필요합니다. 플래시카드 활용을 권장드립니다.",
        "비슷한 단어들을 혼동하는 경우가 있어, 이를 구분하는 연습을 진행할 예정입니다."
    ],
    'reading': [
        "본문 내용을 읽고 이해하는 속도를 높이기 위해 추가 연습이 필요합니다.",
        "긴 문장을 읽을 때 집중력이 흐트러지는 경향이 있어, 단락별로 나누어 학습할 계획입니다.",
        "문맥을 파악하는 능력을 기르기 위해 다양한 지문 연습을 할 예정입니다.",
        "읽기 속도가 조금 느린 편인데, 꾸준한 연습으로 향상될 수 있습니다."
    ],
    'expression': [
        "배운 표현을 실제로 활용하는 데 아직 익숙하지 않아 보입니다. 반복 연습을 통해 자연스러움을 기르겠습니다.",
        "새로운 표현을 문장에 적용하는 연습이 더 필요합니다. 다양한 상황별 예문을 제공할 예정입니다.",
        "표현 확장에서 응용력을 높이기 위해 대화 연습을 늘릴 계획입니다.",
        "일상생활에서 사용할 수 있는 표현 연습에 좀 더 집중하겠습니다."
    ],
    'grammar': [
        "문법 개념 중 시제 구분에서 헷갈려하는 모습이 보였습니다. 현재와 과거 시제의 차이를 더 연습하겠습니다.",
        "주어와 동사의 수일치에서 실수가 있었습니다. 단수/복수 구분 연습을 추가로 진행할 예정입니다.",
        "문장 구조를 파악하는 데 어려움이 있어, 기본 문형부터 차근차근 복습할 계획입니다.",
        "관사(a, an, the) 사용에서 혼란스러워하여 규칙을 정리하여 다시 설명해 드리겠습니다.",
        "의문문 만들기에서 어순이 헷갈린 부분이 있었습니다. 패턴 연습을 통해 익숙해지도록 하겠습니다."
    ],
    'general': [
        "수업 중 집중력이 흐트러지는 순간이 있었습니다. 학습 환경을 개선하여 도움이 되도록 하겠습니다.",
        "과제 완성도를 높이기 위해 시간 관리 방법을 함께 연습해 보겠습니다.",
        "질문하는 것을 조금 어려워하는 모습이 보였는데, 편안하게 질문할 수 있는 분위기를 만들겠습니다.",
        "학습한 내용을 장기 기억으로 전환하기 위해 복습 주기를 조정할 예정입니다."
    ]
}

# 가정학습 제안 템플릿
HOME_STUDY_TEMPLATES = {
    'vocabulary': [
        "오늘 배운 단어들을 하루에 3번씩 소리 내어 읽어보시면 암기에 큰 도움이 됩니다.",
        "단어장을 활용하여 자기 전에 5분 정도 복습하는 습관을 들여주세요.",
        "새 단어로 간단한 문장을 만들어보는 연습을 해보시면 좋겠습니다.",
        "단어를 그림이나 상황과 연결지어 외우면 더 오래 기억할 수 있습니다."
    ],
    'reading': [
        "본문을 소리 내어 읽는 연습을 하루에 2-3회 해주시면 읽기 실력 향상에 효과적입니다.",
        "교재 오디오 파일을 들으며 따라 읽는 쉐도잉 연습을 권장드립니다.",
        "읽은 내용을 간단히 요약해서 말해보는 연습을 해보시면 좋겠습니다.",
        "모르는 단어가 나와도 먼저 문맥으로 뜻을 추측해보는 습관을 길러주세요."
    ],
    'expression': [
        "오늘 배운 표현을 일상에서 사용해볼 수 있도록 격려해 주세요.",
        "가족과 함께 배운 표현으로 간단한 대화를 나눠보시면 큰 도움이 됩니다.",
        "배운 표현을 다양한 상황에 적용해보는 연습을 해보세요.",
        "영어 표현을 자연스럽게 쓸 수 있도록 반복해서 말해보는 시간을 가져주세요."
    ],
    'grammar': [
        "오늘 배운 문법 내용을 활용하여 간단한 일기를 영어로 써보면 좋겠습니다.",
        "문법 규칙을 직접 예문과 함께 정리해보는 연습을 권장드립니다.",
        "교재의 문법 연습 문제를 한 번 더 풀어보시면 이해가 깊어집니다.",
        "배운 문법을 사용하여 3-5개의 문장을 직접 만들어보세요."
    ],
    'encouragement': [
        "아이가 힘들어하거나 지칠 때는 따뜻한 격려의 말씀을 부탁드립니다.",
        "작은 성취에도 칭찬해 주시면 학습 동기 부여에 큰 힘이 됩니다.",
        "영어 학습은 마라톤과 같습니다. 천천히 꾸준히 함께 응원해 주세요.",
        "가정에서의 따뜻한 지지가 아이의 학습에 가장 큰 원동력이 됩니다."
    ],
    'general': [
        "규칙적인 학습 시간을 정해두면 습관 형성에 도움이 됩니다.",
        "학습 후 충분한 휴식을 취하면 배운 내용이 더 잘 정착됩니다.",
        "궁금한 점이 있으시면 언제든지 연락 주세요. 함께 좋은 방법을 찾아보겠습니다.",
        "아이의 학습 페이스를 존중하며 천천히 함께 나아가겠습니다."
    ]
}


def select_unique_phrases(template_list, count, used_phrases=None):
    """중복 없이 문구 선택"""
    if used_phrases is None:
        used_phrases = set()

    available = [p for p in template_list if p not in used_phrases]
    if len(available) < count:
        available = template_list.copy()

    selected = random.sample(available, min(count, len(available)))
    used_phrases.update(selected)
    return selected


def determine_performance_level(data):
    """전체 성적 수준 판단"""
    grades = []
    for key in ['vocabulary', 'reading', 'expression', 'grammar', 'test']:
        if data.get(key):
            grade = data[key].upper() if isinstance(data[key], str) else str(data[key])
            if grade in ['A', 'A+', '100', '95', '90']:
                grades.append(3)
            elif grade in ['B', 'B+', '85', '80', '75']:
                grades.append(2)
            else:
                grades.append(1)

    if not grades:
        return 'good'

    avg = sum(grades) / len(grades)
    if avg >= 2.5:
        return 'excellent'
    elif avg >= 1.5:
        return 'good'
    else:
        return 'needs_improvement'


def generate_report(data):
    """
    Daily Study Report 생성

    Parameters:
    data (dict): 학생 학습 정보
        - name: 학생 이름 (필수)
        - textbook: 교재명 (필수)
        - progress: 진도 (필수)
        - homework: 과제 완성도 (완료/미완료/부분완료)
        - vocabulary: 단어 테스트 등급
        - reading: 본문 테스트 등급
        - expression: 표현확장연습 등급
        - grammar: 문법 테스트 등급
        - test: 전체 테스트 등급
        - notes: 특이사항

    Returns:
    str: 생성된 보고서 텍스트
    """

    name = data.get('name', '학생')
    textbook = data.get('textbook', '')
    progress = data.get('progress', '')
    homework = data.get('homework', '')
    vocabulary = data.get('vocabulary', '')
    reading = data.get('reading', '')
    expression = data.get('expression', '')
    grammar = data.get('grammar', '')
    test = data.get('test', '')
    notes = data.get('notes', '')

    # 보고서 시작
    report = []
    report.append(f"{name} 학생 Daily Study Report 보내드립니다")
    report.append("")

    # 교재 및 진도 현황
    report.append("교재 및 진도 현황")
    report.append(f"사용 교재: {textbook}")
    report.append(f"학습 진도: {progress}")
    report.append("")

    # 학습 평가 결과
    report.append("학습 평가 결과")
    report.append("")

    item_number = 1

    # 1. 과제수행 완성도
    if homework:
        report.append(f"{item_number}. 과제수행 완성도")
        if homework == '완료':
            report.append("(O) 완료 / ( ) 미완료 / ( ) 부분완료")
        elif homework == '미완료':
            report.append("( ) 완료 / (O) 미완료 / ( ) 부분완료")
        elif homework == '부분완료':
            report.append("( ) 완료 / ( ) 미완료 / (O) 부분완료")
        report.append("")
        item_number += 1

    # 2. 단어 테스트 결과
    if vocabulary:
        grade = get_grade_level(vocabulary)
        evaluation = get_grade_evaluation(vocabulary)
        report.append(f"{item_number}. 단어 테스트 결과")
        report.append(f"등급: {grade}")
        report.append(f"평가: {evaluation}")
        report.append("")
        item_number += 1

    # 3. 본문 테스트 결과
    if reading:
        grade = get_grade_level(reading)
        evaluation = get_grade_evaluation(reading)
        report.append(f"{item_number}. 본문 테스트 결과")
        report.append(f"등급: {grade}")
        report.append(f"평가: {evaluation}")
        report.append("")
        item_number += 1

    # 4. 표현확장연습 결과
    if expression:
        grade = get_grade_level(expression)
        evaluation = get_grade_evaluation(expression)
        report.append(f"{item_number}. 표현확장연습 결과")
        report.append(f"등급: {grade}")
        report.append(f"평가: {evaluation}")
        report.append("")
        item_number += 1

    # 5. 문법 테스트 결과
    if grammar:
        grade = get_grade_level(grammar)
        evaluation = get_grade_evaluation(grammar)
        report.append(f"{item_number}. 문법 테스트 결과")
        report.append(f"등급: {grade}")
        report.append(f"평가: {evaluation}")
        report.append("")
        item_number += 1

    # 6. 전체 테스트 결과
    if test:
        grade = get_grade_level(test)
        evaluation = get_grade_evaluation(test)
        report.append(f"{item_number}. 전체 테스트 결과")
        report.append(f"등급: {grade}")
        report.append(f"평가: {evaluation}")
        report.append("")

    # 성적 수준 판단
    performance_level = determine_performance_level(data)
    used_phrases = set()

    # 칭찬할 점 (3~5문장)
    report.append("칭찬할 점")
    praise_phrases = select_unique_phrases(
        PRAISE_TEMPLATES[performance_level],
        random.randint(3, 4),
        used_phrases
    )
    praise_text = ' '.join([p.format(name=name) for p in praise_phrases])

    # 특이사항에서 긍정적인 내용 추가
    if notes and any(keyword in notes for keyword in ['열심히', '잘', '좋', '적극', '발전', '향상']):
        praise_text += f" 특히, {notes}"

    report.append(praise_text)
    report.append("")

    # 개선이 필요한 부분 (3~5문장)
    report.append("개선이 필요한 부분")
    improvement_areas = []

    if vocabulary and get_grade_evaluation(vocabulary) != '우수':
        improvement_areas.append('vocabulary')
    if reading and get_grade_evaluation(reading) != '우수':
        improvement_areas.append('reading')
    if expression and get_grade_evaluation(expression) != '우수':
        improvement_areas.append('expression')
    if grammar and get_grade_evaluation(grammar) != '우수':
        improvement_areas.append('grammar')

    if not improvement_areas:
        improvement_areas = ['general']

    improvement_phrases = []
    for area in improvement_areas[:2]:
        phrases = select_unique_phrases(IMPROVEMENT_TEMPLATES[area], 1, used_phrases)
        improvement_phrases.extend(phrases)

    if len(improvement_phrases) < 3:
        additional = select_unique_phrases(IMPROVEMENT_TEMPLATES['general'], 3 - len(improvement_phrases), used_phrases)
        improvement_phrases.extend(additional)

    improvement_text = ' '.join(improvement_phrases)

    # 특이사항에서 개선 관련 내용 추가
    if notes and any(keyword in notes for keyword in ['어려', '힘들', '부족', '실수', '헷갈']):
        improvement_text += f" {notes}와 관련하여 추가 지도를 진행할 예정입니다."

    report.append(improvement_text)
    report.append("")

    # 가정에서의 학습 제안 (3~5문장)
    report.append("가정에서의 학습 제안")
    home_study_areas = improvement_areas[:2] if improvement_areas else ['general']

    home_study_phrases = []
    for area in home_study_areas:
        if area in HOME_STUDY_TEMPLATES:
            phrases = select_unique_phrases(HOME_STUDY_TEMPLATES[area], 1, used_phrases)
            home_study_phrases.extend(phrases)

    # 격려 문구 추가
    encouragement = select_unique_phrases(HOME_STUDY_TEMPLATES['encouragement'], 1, used_phrases)
    home_study_phrases.extend(encouragement)

    # 일반 제안 추가
    if len(home_study_phrases) < 3:
        general = select_unique_phrases(HOME_STUDY_TEMPLATES['general'], 3 - len(home_study_phrases), used_phrases)
        home_study_phrases.extend(general)

    home_study_text = ' '.join(home_study_phrases)
    report.append(home_study_text)

    return '\n'.join(report)


def save_report(report_text, filename=None):
    """보고서를 파일로 저장"""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"daily_report_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_text)

    return filename


# 테스트용 코드
if __name__ == '__main__':
    # 예시 데이터
    sample_data = {
        'name': '홍길동',
        'textbook': 'Orange 8',
        'progress': 'Day 7',
        'homework': '완료',
        'vocabulary': 'A',
        'reading': 'B',
        'expression': 'B+',
        'grammar': 'C',
        'test': 'B',
        'notes': '문법 시제 부분에서 현재와 과거를 헷갈려했으나 열심히 노력하는 모습이 보였습니다'
    }

    report = generate_report(sample_data)
    print(report)
    print("\n" + "="*50 + "\n")

    # 파일로 저장
    saved_file = save_report(report)
    print(f"보고서가 {saved_file}에 저장되었습니다.")
