from tkinter import *

QUESTIONS = [
    "Thao tác Thêm",
    "Thao tác Xoá",
    "Thao tác Sửa",
    "Xuất file CSV",
    "Nút Reset có tác dụng gì?", 
    "Nút Huỷ có tác dụng gì?",
]

ANSWERS = [
    "Nhấn nút 'Thêm' để thêm nhân viên mới. Điền mã NV, họ tên và thông tin cần thiết, sau đó nhấn 'Lưu'.",
    "Chọn nhân viên muốn xoá trên bảng rồi nhấn nút 'Xóa'. Hệ thống sẽ xác nhận trước khi xóa.",
    "Chọn nhân viên cần sửa rồi nhấn 'Sửa'. Cập nhật thông tin và nhấn 'Lưu'.",
    "Nhấn 'Xuất CSV' để xuất dữ liệu ra file CSV. File này có thể mở bằng Excel.",
    "Nút 'Reset' có tác dụng làm mới hệ thống, đưa chatbot về trạng thái ban đầu.",
    "Nút 'Huỷ' có tác dụng làm mới các ô entry, ngừng các thao tác Thêm/Xoá/Sửa đang thực hiện.",
]

def open_chatbot(parent):
    win = Toplevel(parent)
    win.title("Hỗ trợ ChatBot")
    win.geometry("400x600")
    win.resizable(False, False)

    # ===== Text hiển thị câu trả lời =====
    frame_text = Frame(win)
    frame_text.pack(fill="both", expand=True,pady=5)

    scrollbar_text = Scrollbar(frame_text)
    scrollbar_text.pack(side=RIGHT, fill=Y)

    txt_display = Text(frame_text, wrap="word", yscrollcommand=scrollbar_text.set, font=("Arial", 10))
    txt_display.pack(fill="both", expand=True)
    scrollbar_text.config(command=txt_display.yview)

    txt_display.insert(END, "Chọn 1 câu hỏi bên dưới để xem hướng dẫn:\n\n")
    txt_display.config(state="disabled")

    # ===== Canvas scrollable cho các nút câu hỏi =====
    canvas_frame = Frame(win)
    canvas_frame.pack(fill="both", pady=5, expand=False)

    canvas = Canvas(canvas_frame, height=150)
    canvas.pack(side=LEFT, fill="both", expand=True)

    scrollbar_btn = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar_btn.pack(side=RIGHT, fill=Y)

    btn_frame = Frame(canvas)
    canvas.create_window((0,0), window=btn_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_btn.set)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    btn_frame.bind("<Configure>", on_frame_configure)

    # ===== Hiển thị câu trả lời =====
    def show_answer(i):
        txt_display.config(state="normal")
        txt_display.insert(END, f"• {QUESTIONS[i]}\n→ {ANSWERS[i]}\n\n")
        txt_display.see(END)
        txt_display.config(state="disabled")

    # ===== Reset =====
    def reset_chat():
        txt_display.config(state="normal")
        txt_display.delete(1.0, END)
        txt_display.insert(END, "Chọn 1 câu hỏi bên dưới để xem hướng dẫn:\n\n")
        txt_display.config(state="disabled")

    # ===== Tạo các nút câu hỏi =====
    for i, q in enumerate(QUESTIONS):
        Button(btn_frame, text=q, width=40, anchor="w",
               command=lambda i=i: show_answer(i),
               relief="groove", bg="#E6F2FA", fg="#2F4156").pack(pady=2, fill="x")

    # Nút Reset luôn hiển thị bên dưới
    Button(win, text="🔄 Reset", width=40, anchor="w",command=reset_chat, relief="groove", bg="#FF6B6B", fg="white").pack(pady=5, fill="x")

    return win

def add_chatbot_button(parent, x_offset=-10, y_offset=30):
    btn = Button(parent, text="💬", width=3, height=2, command=lambda: open_chatbot(parent), bg="#00AEEF", fg="white", bd=0, relief="raised", cursor="hand2")
    btn.place(relx=1.0, x=x_offset, y=y_offset, anchor="ne")

    return btn
