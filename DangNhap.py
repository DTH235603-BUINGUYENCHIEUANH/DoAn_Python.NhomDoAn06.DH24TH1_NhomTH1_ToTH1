from tkinter import *
import tkinter as tk
from tkinter import messagebox
from QLKS import conn, cur, connect_db
from TrangChu import open_trang_chu
import mysql.connector

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=400, h=400):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')   

def DangNhap():  # xử lý btn Đăng Nhập
    ten = TenDangNhap_entry.get()
    matkhau = MatKhau_entry.get()
    xacnhan = confirm_entry.get()

    if not ten or not matkhau or not xacnhan:
        messagebox.showwarning("Vui lòng điền đầy đủ thông tin.", "Thông báo")
    elif matkhau != xacnhan:
        messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp.")
        confirm_entry.focus_set()   
        cur.close()
    else:
        # ====== Kết nối MySQL ======
        try:
            conn = connect_db()
            cur = conn.cursor()

            # Kiểm tra người dùng tồn tại không
            query = "SELECT * FROM nguoidung WHERE TenNguoiDung = %s AND MatKhau = %s"
            cur.execute(query, (ten, matkhau))
            user = cur.fetchone()

            if user:
                vaitro = user[3]
                messagebox.showinfo("Thành công", f"Đăng nhập thành công với tài khoản: {ten} ({vaitro})")
                frmDangNhap.destroy()      # Đóng cửa sổ đăng nhập
                open_trang_chu(vaitro)           # Mở giao diện Trang Chủ
            else:
                messagebox.showerror("Thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối CSDL: {e}")
    
    


# Tạo giao diện chính
frmDangNhap = Tk()
frmDangNhap.title("Đăng Nhập Hệ Thống Quản Lý Khách Sạn")
frmDangNhap.minsize(width=400, height=400)
center_window(frmDangNhap)
frmDangNhap.configure(bg="#E6F2FA")

# lab_ Đăng Nhập
lab_DangNhap = Label(frmDangNhap, text="ĐĂNG NHẬP HỆ THỐNG",font=("Times New Roman", 20, "bold"), foreground="#2F4156", bg="#E6F2FA")
lab_DangNhap.pack(pady=(30, 5))

subtitle = Label(frmDangNhap,text="WELLCOME HỆ THỐNG QUẢN LÝ KHÁCH SẠN TOM&JERRY",font=("Times New Roman", 10), foreground="#2F4156", bg="#E6F2FA")
subtitle.pack(pady=(0, 20))

# lab Tên đăng nhập + entry
lab_TenDangNhap = Label(frmDangNhap,text="Tên đăng nhập: ", font=("Times New Roman", 12), foreground="#2F4156", bg="#E6F2FA",anchor="w")
lab_TenDangNhap.pack(fill="x", padx=50)
TenDangNhap_entry = Entry(frmDangNhap,font=("Times New Roman", 12),width=30)
TenDangNhap_entry.pack(pady=5)

# lab + entry mật khẩu
lab_MatKhau = Label(frmDangNhap, text="Mật khẩu: ", font=("Times New Roman", 12), foreground="#2F4156", bg="#E6F2FA", anchor="w")
lab_MatKhau.pack(fill="x", padx=50)
MatKhau_entry = Entry(frmDangNhap, font=("Times New Roman", 12), width=30, show="*")
MatKhau_entry.pack(pady=5)

# lab + entry xác nhận mật khẩu
lab_XacNhan = Label(frmDangNhap, text="Nhập lại mật khẩu: ", font=("Times New Roman", 12), foreground="#2F4156", bg="#E6F2FA", anchor="w")
lab_XacNhan.pack(fill="x", padx=50)
confirm_entry = Entry(frmDangNhap, font=("Times New Roman", 12), width=30, show="*")
confirm_entry.pack(pady=5)

# btn Đăng Nhập
Dangnhap_btn = Button(frmDangNhap, text="Đăng Nhập", font=("Times New Roman", 12), bg="#00AEEF", foreground="white", width=20,command=DangNhap)
Dangnhap_btn.pack(pady=20)

# Chạy giao diện
frmDangNhap.mainloop()
