"""
Daily Study Report 데스크톱 앱
학생 정보를 입력하면 보고서를 생성하고 바로 복사할 수 있습니다.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

# 등급 평가 함수
def get_grade_evaluation(grade):
    if grade in ['A', 'A+']:
        return '우수'
    elif grade in ['B', 'B+']:
        return '보통'
    elif grade in ['C', 'C+', 'D', 'F']:
        return '미흡'
    return ''

def generate_report():
    """보고서 생성"""
    name = entry_name.get().strip()
    textbook = entry_textbook.get().strip()
    progress = entry_progress.get().strip()

    if not all([name, textbook, progress]):
        messagebox.showwarning("입력 오류", "학생 이름, 교재, 진도는 필수입니다.")
        return

    homework = combo_homework.get()
    vocabulary = combo_vocabulary.get()
    reading = combo_reading.get()
    expression = combo_expression.get()
    grammar = combo_grammar.get()
    test = combo_test.get()
    notes = text_notes.get("1.0", tk.END).strip()

    # 보고서 작성
    report = []
    report.append(f"{name} 학생 Daily Study Report 보내드립니다")
    report.append("")
    report.append("교재 및 진도 현황")
    report.append(f"사용 교재: {textbook}")
    report.append(f"학습 진도: {progress}")
    report.append("")
    report.append("학습 평가 결과")
    report.append("")

    item_num = 1

    # 과제수행 완성도
    if homework:
        report.append(f"{item_num}. 과제수행 완성도")
        if homework == '완료':
            report.append("(O) 완료 / ( ) 미완료 / ( ) 부분완료")
        elif homework == '미완료':
            report.append("( ) 완료 / (O) 미완료 / ( ) 부분완료")
        elif homework == '부분완료':
            report.append("( ) 완료 / ( ) 미완료 / (O) 부분완료")
        report.append("")
        item_num += 1

    # 단어 테스트
    if vocabulary:
        report.append(f"{item_num}. 단어 테스트 결과")
        report.append(f"등급: {vocabulary}")
        report.append(f"평가: {get_grade_evaluation(vocabulary)}")
        report.append("")
        item_num += 1

    # 본문 테스트
    if reading:
        report.append(f"{item_num}. 본문 테스트 결과")
        report.append(f"등급: {reading}")
        report.append(f"평가: {get_grade_evaluation(reading)}")
        report.append("")
        item_num += 1

    # 표현확장연습
    if expression:
        report.append(f"{item_num}. 표현확장연습 결과")
        report.append(f"등급: {expression}")
        report.append(f"평가: {get_grade_evaluation(expression)}")
        report.append("")
        item_num += 1

    # 문법 테스트
    if grammar:
        report.append(f"{item_num}. 문법 테스트 결과")
        report.append(f"등급: {grammar}")
        report.append(f"평가: {get_grade_evaluation(grammar)}")
        report.append("")
        item_num += 1

    # 전체 테스트
    if test:
        report.append(f"{item_num}. 전체 테스트 결과")
        report.append(f"등급: {test}")
        report.append(f"평가: {get_grade_evaluation(test)}")
        report.append("")

    # 칭찬할 점, 개선점, 가정학습 제안은 특이사항 기반으로 작성 필요
    report.append("칭찬할 점")
    report.append("[직접 작성해 주세요]")
    report.append("")
    report.append("개선이 필요한 부분")
    report.append("[직접 작성해 주세요]")
    report.append("")
    report.append("가정에서의 학습 제안")
    report.append("[직접 작성해 주세요]")

    if notes:
        report.append("")
        report.append(f"[참고 - 특이사항: {notes}]")

    result = "\n".join(report)

    # 결과 표시
    text_result.config(state=tk.NORMAL)
    text_result.delete("1.0", tk.END)
    text_result.insert("1.0", result)
    text_result.config(state=tk.DISABLED)

    btn_copy.config(state=tk.NORMAL)

def copy_to_clipboard():
    """클립보드에 복사"""
    result = text_result.get("1.0", tk.END).strip()
    if result:
        try:
            pyperclip.copy(result)
            messagebox.showinfo("복사 완료", "클립보드에 복사되었습니다!")
        except:
            # pyperclip이 없는 경우 tkinter 클립보드 사용
            root.clipboard_clear()
            root.clipboard_append(result)
            messagebox.showinfo("복사 완료", "클립보드에 복사되었습니다!")

def clear_form():
    """폼 초기화"""
    entry_name.delete(0, tk.END)
    entry_textbook.delete(0, tk.END)
    entry_progress.delete(0, tk.END)
    combo_homework.set('')
    combo_vocabulary.set('')
    combo_reading.set('')
    combo_expression.set('')
    combo_grammar.set('')
    combo_test.set('')
    text_notes.delete("1.0", tk.END)
    text_result.config(state=tk.NORMAL)
    text_result.delete("1.0", tk.END)
    text_result.config(state=tk.DISABLED)
    btn_copy.config(state=tk.DISABLED)

# 메인 윈도우
root = tk.Tk()
root.title("Daily Study Report 작성기")
root.geometry("800x700")
root.resizable(True, True)

# 스타일 설정
style = ttk.Style()
style.configure('TLabel', font=('맑은 고딕', 10))
style.configure('TButton', font=('맑은 고딕', 10))
style.configure('Header.TLabel', font=('맑은 고딕', 14, 'bold'))

# 메인 프레임
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# 헤더
header_label = ttk.Label(main_frame, text="Daily Study Report 작성기", style='Header.TLabel')
header_label.pack(pady=(0, 15))

# 입력 프레임
input_frame = ttk.LabelFrame(main_frame, text="학생 정보 입력", padding="10")
input_frame.pack(fill=tk.X, pady=(0, 10))

# 기본 정보
row1 = ttk.Frame(input_frame)
row1.pack(fill=tk.X, pady=5)

ttk.Label(row1, text="학생 이름*", width=12).pack(side=tk.LEFT)
entry_name = ttk.Entry(row1, width=15)
entry_name.pack(side=tk.LEFT, padx=(0, 20))

ttk.Label(row1, text="교재*", width=8).pack(side=tk.LEFT)
entry_textbook = ttk.Entry(row1, width=25)
entry_textbook.pack(side=tk.LEFT, padx=(0, 20))

ttk.Label(row1, text="진도*", width=8).pack(side=tk.LEFT)
entry_progress = ttk.Entry(row1, width=15)
entry_progress.pack(side=tk.LEFT)

# 평가 정보
row2 = ttk.Frame(input_frame)
row2.pack(fill=tk.X, pady=5)

grades = ['', 'A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']
homework_options = ['', '완료', '부분완료', '미완료']

ttk.Label(row2, text="과제", width=12).pack(side=tk.LEFT)
combo_homework = ttk.Combobox(row2, values=homework_options, width=10, state='readonly')
combo_homework.pack(side=tk.LEFT, padx=(0, 20))

ttk.Label(row2, text="단어", width=8).pack(side=tk.LEFT)
combo_vocabulary = ttk.Combobox(row2, values=grades, width=8, state='readonly')
combo_vocabulary.pack(side=tk.LEFT, padx=(0, 20))

ttk.Label(row2, text="본문", width=8).pack(side=tk.LEFT)
combo_reading = ttk.Combobox(row2, values=grades, width=8, state='readonly')
combo_reading.pack(side=tk.LEFT)

row3 = ttk.Frame(input_frame)
row3.pack(fill=tk.X, pady=5)

ttk.Label(row3, text="표현", width=12).pack(side=tk.LEFT)
combo_expression = ttk.Combobox(row3, values=grades, width=10, state='readonly')
combo_expression.pack(side=tk.LEFT, padx=(0, 20))

ttk.Label(row3, text="문법", width=8).pack(side=tk.LEFT)
combo_grammar = ttk.Combobox(row3, values=grades, width=8, state='readonly')
combo_grammar.pack(side=tk.LEFT, padx=(0, 20))

ttk.Label(row3, text="테스트", width=8).pack(side=tk.LEFT)
combo_test = ttk.Combobox(row3, values=grades, width=8, state='readonly')
combo_test.pack(side=tk.LEFT)

# 특이사항
row4 = ttk.Frame(input_frame)
row4.pack(fill=tk.X, pady=5)

ttk.Label(row4, text="특이사항", width=12).pack(side=tk.LEFT, anchor=tk.N)
text_notes = tk.Text(row4, height=3, width=60, font=('맑은 고딕', 10))
text_notes.pack(side=tk.LEFT, fill=tk.X, expand=True)

# 버튼 프레임
btn_frame = ttk.Frame(main_frame)
btn_frame.pack(fill=tk.X, pady=10)

btn_generate = ttk.Button(btn_frame, text="보고서 생성", command=generate_report)
btn_generate.pack(side=tk.LEFT, padx=5)

btn_copy = ttk.Button(btn_frame, text="복사하기", command=copy_to_clipboard, state=tk.DISABLED)
btn_copy.pack(side=tk.LEFT, padx=5)

btn_clear = ttk.Button(btn_frame, text="초기화", command=clear_form)
btn_clear.pack(side=tk.LEFT, padx=5)

# 결과 프레임
result_frame = ttk.LabelFrame(main_frame, text="생성된 보고서", padding="10")
result_frame.pack(fill=tk.BOTH, expand=True)

text_result = tk.Text(result_frame, height=15, font=('맑은 고딕', 10), state=tk.DISABLED)
text_result.pack(fill=tk.BOTH, expand=True)

# 스크롤바
scrollbar = ttk.Scrollbar(text_result, orient=tk.VERTICAL, command=text_result.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_result.config(yscrollcommand=scrollbar.set)

# 안내 메시지
info_label = ttk.Label(main_frame, text="* 표시는 필수 입력 항목입니다. 칭찬/개선/가정학습 부분은 직접 수정해 주세요.",
                       font=('맑은 고딕', 9), foreground='gray')
info_label.pack(pady=(5, 0))

root.mainloop()
