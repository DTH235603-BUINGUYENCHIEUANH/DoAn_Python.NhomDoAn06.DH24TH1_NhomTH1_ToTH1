from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur
from DatPhong import open_form_datphong
from DatDichVu import open_form_datdichvu
from DichVu import open_form_dichvu
from Phong import open_form_phong
from ThanhToan import open_form_thanhtoan
from DanhSachKH import open_form_khachhang


def open_trang_chu():
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
        img_label.image = photo  # Giữ tham chiếu
        img_label.pack()
    except Exception as e:
        Label(frame_Image, text="Không thể tải ảnh", bg="#E6F2FA", fg="red").pack()

    # ==== Tên + Địa chỉ bên phải ====
    frame_Info = Frame(frame_Top, bg="#E6F2FA")
    Label(frame_Info, text="HỆ THỐNG QUẢN LÝ KHÁCH SẠN", font=("Times New Roman", 16), bg="#E6F2FA", foreground="#2F4156").pack(anchor="center", padx=10, pady=10)
    Label(frame_Info, text="TOM AND JERRY", font=("Times New Roman", 20, "bold"), bg="#E6F2FA", foreground="#2F4156").pack(anchor="center", padx=10, pady=10)
    Label(frame_Info, text="Dien Bien Phu, Ha Tien, An Giang", font=("Times New Roman", 16), bg="#E6F2FA", foreground="#2F4156").pack(anchor="center", padx=10, pady=10)
    frame_Info.pack(side=RIGHT, anchor=CENTER)

    # ==== Button phía dưới ====
    frame_Button = Frame(trangchu, bg="#E6F2FA")
    Button(frame_Button, text="Dịch vụ", font=("Times New Roman", 14), background="#F5EFEB", foreground="#2F4156", command=open_form_dichvu).pack(side=LEFT, padx=10)
    Button(frame_Button, text="Phòng", font=("Times New Roman", 14), background="#F5EFEB", foreground="#2F4156", command=open_form_phong).pack(side=LEFT, padx=10) #
    Button(frame_Button, text="Đặt phòng", font=("Times New Roman", 14), background="#F5EFEB", foreground="#2F4156", command=open_form_datphong).pack(side=LEFT, padx=10)
    Button(frame_Button, text="Đặt dịch vụ", font=("Times New Roman", 14), background="#F5EFEB", foreground="#2F4156", command=open_form_datdichvu).pack(side=LEFT, padx=10) #
    Button(frame_Button, text="Thanh toán", font=("Times New Roman", 14), background="#F5EFEB", foreground="#2F4156", command=open_form_thanhtoan).pack(side=LEFT, padx=10)
    Button(frame_Button, text="Danh sách khách hàng", font=("Times New Roman", 14), background="#F5EFEB", foreground="#2F4156", command=open_form_khachhang).pack(side=LEFT, padx=10)


    frame_Button.grid(row=1, column=0, columnspan=2, sticky="s", pady=10)
    trangchu.mainloop()

