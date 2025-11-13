from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur
from DatPhong import open_form_DatPhong
from DatDichVu import open_form_DatDichVu
from DichVu import open_form_DichVu
from Phong import open_form_Phong
from ThanhToan import open_form_ThanhToan
from DanhSachKH import open_form_DanhSachKH
from NhanVien import open_form_NhanVien

def open_trang_chu(vaitro):
    # ====== Hàm canh giữa cửa sổ ======
    def center_window(win, w=700, h=500):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')
    # ===== Cửa sổ chính =====
    trangchu = Tk()
    trangchu.title("Trang chủ - Quản lý khách sạn")
    trangchu.minsize(width=800, height=400)
    center_window(trangchu)
    trangchu.configure(bg="#E6F2FA")

    # ===== Khung tổng chứa ảnh + thông tin =====
    frame_Top = Frame(trangchu, bg="#E6F2FA")
    frame_Top.grid(row=0, rowspan=2, column=0, padx=20, pady=20)

    # ==== Ảnh bên trái ====
    frame_Image = Frame(frame_Top, bg="#E6F2FA")
    frame_Image.pack(side=LEFT, padx=10)

    try:
        image = Image.open("img/hotel1.jpg")  # Đường dẫn ảnh
        image = image.resize((300, 400))
        photo = ImageTk.PhotoImage(image)
        img_label = Label(frame_Image, image=photo)
        img_label.image = photo  # tham chiếu
        img_label.pack()
    except Exception as e:
        Label(frame_Image, text="Không thể tải ảnh", bg="#E6F2FA", fg="red").pack()

    # ==== Tên + Địa chỉ bên phải ====
    frame_Info = Frame(frame_Top, bg="#E6F2FA")
    Label(frame_Info, text="HỆ THỐNG QUẢN LÝ KHÁCH SẠN", font=("Times New Roman", 16), bg="#E6F2FA", foreground="#2F4156").pack(anchor="center", padx=10, pady=10)
    Label(frame_Info, text="TOM AND JERRY", font=("Times New Roman", 20, "bold"), bg="#E6F2FA", foreground="#2F4156").pack(anchor="center", padx=10, pady=10)
    Label(frame_Info, text="Dien Bien Phu, Ha Tien, An Giang", font=("Times New Roman", 16), bg="#E6F2FA", foreground="#2F4156").pack(anchor="center", padx=10, pady=10)
    frame_Info.pack(side=RIGHT, anchor=CENTER)

    # ===== Frame Button =====
    frame_Button = Frame(trangchu, bg="#E6F2FA")
    frame_Button.grid(row=1, column=0, columnspan=2, sticky="s", pady=10, padx=5)

    # ===== Hàng 1: Các nút ngắn =====
    frame_row1 = Frame(frame_Button, bg="#E6F2FA")
    frame_row1.pack(pady=5)

    Button(frame_row1, text="Dịch vụ", font=("Times New Roman", 14), width=8,bg="#00AEEF", fg="white", command=lambda:open_form_DichVu(vaitro)).pack(side=LEFT, padx=10)

    Button(frame_row1, text="Phòng", font=("Times New Roman", 14), width=8, bg="#00AEEF", fg="white", command=lambda:open_form_Phong(vaitro)).pack(side=LEFT, padx=10)

    Button(frame_row1, text="Đặt phòng", font=("Times New Roman", 14), width=10, bg="#00AEEF", fg="white", command=lambda:open_form_DatPhong(vaitro)).pack(side=LEFT, padx=10)

    Button(frame_row1, text="Đặt dịch vụ", font=("Times New Roman", 14), width=10, bg="#00AEEF", fg="white", command=lambda:open_form_DatDichVu(vaitro)).pack(side=LEFT, padx=10)

    Button(frame_row1, text="Thanh toán", font=("Times New Roman", 14), width=10, bg="#00AEEF", fg="white", command=lambda:open_form_ThanhToan(vaitro)).pack(side=LEFT, padx=10)


    # ===== Hàng 2: Hai nút dài =====
    frame_row2 = Frame(frame_Button, bg="#E6F2FA")
    frame_row2.pack(pady=10)

    Button(frame_row2, text="Danh sách khách hàng", font=("Times New Roman", 14), width=22, bg="#00AEEF", fg="white", command=lambda:open_form_DanhSachKH(vaitro)).pack(side=LEFT, padx=10)
    Button(frame_row2, text="Danh sách nhân viên", font=("Times New Roman", 14), width=22, bg="#00AEEF", fg="white", command=lambda: open_form_NhanVien(vaitro)).pack(side=LEFT, padx=10)

    trangchu.mainloop()

