from tkinter import *
import importlib

def create_menu(parent, current_name, vaitro):
    # ===== Danh sách các nút menu =====
    menu_items = [
        ("Phong", "Phòng"),
        ("DichVu", "Dịch vụ"),
        ("DatDichVu", "Đặt dịch vụ"),
        ("DatPhong", "Đặt phòng"),
        ("ThanhToan", "Thanh toán"),
        ("DanhSachKH", "DS Khách hàng"),
        ("NhanVien", "DS Nhân viên")
    ]

    # ===== Frame chứa thanh menu =====
    menu_frame = Frame(parent, bg="#00AEEF", height=40)
    menu_frame.pack(fill="x")

    # ===== Hàm chuyển form =====
    def switch_form(form_name):
        parent.destroy()
        try:
            module = importlib.import_module(f"{form_name}")  # dùng form_name, không phải name
            func = getattr(module, f"open_form_{form_name}")  # hàm mở form theo tên file
            func(vaitro)
        except ModuleNotFoundError:
            print(f"Lỗi: Không tìm thấy file {form_name}.py")
        except AttributeError:
            print(f"Lỗi: Không tìm thấy hàm open_form_{form_name} trong {form_name}.py")


    # ===== Tạo các nút menu =====
    for name, text in menu_items:
        bg_color = "#0090D0" if name == current_name else "#00AEEF"
        btn = Button(
            menu_frame, text=text, bg=bg_color, fg="white",
            relief="flat", font=("Arial", 11, "bold"),
            activebackground="#007AA3", activeforeground="white",
            cursor="hand2",
            command=lambda n=name: switch_form(n)
        )
        btn.pack(side=LEFT, padx=2, pady=3)

    # Hiển thị vai trò người dùng bên phải
    Label(menu_frame, text=f"Vai trò: {vaitro}", bg="#00AEEF", fg="white", font=("Arial", 10, "italic")).pack(side=RIGHT, padx=10)
