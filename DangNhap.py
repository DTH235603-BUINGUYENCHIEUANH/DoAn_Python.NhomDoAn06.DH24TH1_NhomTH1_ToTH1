import tkinter as tk
from tkinter import messagebox


def DangNhap():  # xử lý btn Đăng Nhập
    ten = TenDangNhap_entry.get()
    matkhau = MatKhau_entry.get()
    xacnhan = confirm_entry.get()

    if not ten or not matkhau or not xacnhan:
        messagebox.showwarning(
            "Thiếu thông tin", 
            "Vui lòng điền đầy đủ thông tin.")
    elif matkhau != xacnhan:
        messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp.")
    else:
        messagebox.showinfo(
            "Thành công", 
            f"Đăng nhập thành công với tài khoản: {ten}")


# Tạo giao diện chính
frmDangNhap = tk.Tk()
frmDangNhap.title("Đăng Nhập Hệ Thống Quản Lý Khách Sạn")
frmDangNhap.geometry("400x400")
frmDangNhap.configure(bg="#E6F2FA")

# lab_ Đăng Nhập
lab_DangNhap = tk.Label(
    frmDangNhap, 
    text="ĐĂNG NHẬP HỆ THỐNG",
    font=("Times New Roman", 20, "bold"),
    bg="#E6F2FA"
)
lab_DangNhap.pack(pady=(30, 5))

subtitle = tk.Label(
    frmDangNhap,
    text="WELLCOME HỆ THỐNG QUẢN LÝ KHÁCH SẠN TOM&JERRY",
    font=("Times New Roman", 10),
    bg="#E6F2FA"
)
subtitle.pack(pady=(0, 20))

# lab Tên đăng nhập + entry
lab_TenDangNhap = tk.Label(
    frmDangNhap,
    text="Tên đăng nhập: ",
    font=("Times New Roman", 12),
    bg="#E6F2FA",
    anchor="w"
)
lab_TenDangNhap.pack(fill="x", padx=50)
TenDangNhap_entry = tk.Entry(
    frmDangNhap,
    font=("Times New Roman", 12),
    width=30
)
TenDangNhap_entry.pack(pady=5)

# lab + entry mật khẩu
lab_MatKhau = tk.Label(
    frmDangNhap,
    text="Mật khẩu: ",
    font=("Times New Roman", 12),
    bg="#E6F2FA",
    anchor="w"
)
lab_MatKhau.pack(fill="x", padx=50)
MatKhau_entry = tk.Entry(
    frmDangNhap,
    font=("Times New Roman", 12),
    width=30,
    show="*"
)
MatKhau_entry.pack(pady=5)

# lab + entry xác nhận mật khẩu
lab_XacNhan = tk.Label(
    frmDangNhap,
    text="Nhập lại mật khẩu: ",
    font=("Times New Roman", 12),
    bg="#E6F2FA",
    anchor="w"
)
lab_XacNhan.pack(fill="x", padx=50)
confirm_entry = tk.Entry(
    frmDangNhap,
    font=("Times New Roman", 12),
    width=30,
    show="*"
)
confirm_entry.pack(pady=5)

# btn Đăng Nhập
Dangnhap_btn = tk.Button(
    frmDangNhap,
    text="Đăng Nhập",
    font=("Times New Roman", 12),
    bg="#00AEEF",
    fg="white",
    width=20,
    command=DangNhap
)
Dangnhap_btn.pack(pady=20)

# Chạy giao diện
frmDangNhap.mainloop()