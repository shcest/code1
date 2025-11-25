"""
Daily Study Report 데스크톱 앱
학생 정보를 입력하면 AI가 자동으로 보고서를 생성하고 바로 복사할 수 있습니다.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from report_generator import generate_report

def create_report():
    """보고서 생성"""
    name = entry_name.get().strip()
    textbook = entry_textbook.get().strip()
    progress = entry_progress.get().strip()

    if not all([name, textbook, progress]):
        messagebox.showwarning("입력 오류", "학생 이름, 교재, 진도는 필수입니다.")
        return

    # 보고서 데이터 구성
    report_data = {
        'name': name,
        'textbook': textbook,
        'progress': progress,
        'homework': combo_homework.get(),
        'vocabulary': combo_vocabulary.get(),
        'reading': combo_reading.get(),
        'expression': combo_expression.get(),
        'grammar': combo_grammar.get(),
        'test': combo_test.get(),
        'notes': text_notes.get("1.0", tk.END).strip()
    }

    # AI 자동 생성
    result = generate_report(report_data)

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
            import pyperclip
            pyperclip.copy(result)
        except:
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
root.geometry("850x750")
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
text_notes = tk.Text(row4, height=4, width=60, font=('맑은 고딕', 10))
text_notes.pack(side=tk.LEFT, fill=tk.X, expand=True)

# 특이사항 안내
note_info = ttk.Label(input_frame,
    text="특이사항에 칭찬할 점, 개선할 점, 가정학습 관련 내용을 입력하면 보고서에 자동 반영됩니다.",
    font=('맑은 고딕', 9), foreground='#666666')
note_info.pack(anchor=tk.W, pady=(5, 0))

# 버튼 프레임
btn_frame = ttk.Frame(main_frame)
btn_frame.pack(fill=tk.X, pady=10)

btn_generate = ttk.Button(btn_frame, text="보고서 생성", command=create_report)
btn_generate.pack(side=tk.LEFT, padx=5)

btn_copy = ttk.Button(btn_frame, text="복사하기", command=copy_to_clipboard, state=tk.DISABLED)
btn_copy.pack(side=tk.LEFT, padx=5)

btn_clear = ttk.Button(btn_frame, text="초기화", command=clear_form)
btn_clear.pack(side=tk.LEFT, padx=5)

# 결과 프레임
result_frame = ttk.LabelFrame(main_frame, text="생성된 보고서 (AI 자동 작성)", padding="10")
result_frame.pack(fill=tk.BOTH, expand=True)

# 결과 텍스트와 스크롤바
result_container = ttk.Frame(result_frame)
result_container.pack(fill=tk.BOTH, expand=True)

text_result = tk.Text(result_container, height=18, font=('맑은 고딕', 10), state=tk.DISABLED, wrap=tk.WORD)
text_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(result_container, orient=tk.VERTICAL, command=text_result.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_result.config(yscrollcommand=scrollbar.set)

# 안내 메시지
info_label = ttk.Label(main_frame,
    text="* 표시는 필수 입력 항목입니다. 보고서 생성 후 필요시 직접 수정하실 수 있습니다.",
    font=('맑은 고딕', 9), foreground='gray')
info_label.pack(pady=(5, 0))

root.mainloop()
