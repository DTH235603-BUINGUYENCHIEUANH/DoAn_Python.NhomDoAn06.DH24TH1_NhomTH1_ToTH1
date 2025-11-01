from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import connect_db

# ===== Cửa sổ chính =====
hoadon = Tk()
hoadon.title("Hoá đơn - Quản lý khách sạn")
hoadon.minsize(width=600, height=500)
hoadon.configure(bg="#E6F2FA")

# ==== Title ====
frame_Title = Frame(hoadon)
Label(frame_Title, text="HỆ THỐNG HOÁ ĐƠN KHÁCH SẠN TOM AND JERRY", font=("Time news roman",20, "bold"), foreground="#2F4156", background="#E6F2FA").pack()
frame_Title.pack(pady=20, padx=10, fill="x", anchor=CENTER)
frame_Title.configure(bg="#E6F2FA")

# ==== Frame nhập thông tin ==== 
frame_Info = Frame(hoadon)
label_mahd = Label(
    frame_Info, 
    text="Mã hoá đơn: ", 
    font=("Time news roman",14,"bold"), 
    foreground="#2F4156", background="#E6F2FA").grid(row=0, column=0)
entry_mahd = Entry(frame_Info, width=10).grid(row=0, column=1)

label_manvtt = Label(
    frame_Info, 
    text="Mã NV Thanh toán: ", 
    font=("Time news roman",14,"bold"), 
    foreground="#2F4156", background="#E6F2FA").grid(row=1, column=0)
entry_manvtt = Entry(frame_Info, width=20).grid(row=1, column=1)

label_makh = Label(
    frame_Info, 
    text="Mã khách hàng: ", 
    font=("Time news roman",14,"bold"), 
    foreground="#2F4156", 
    background="#E6F2FA").grid(row=2, column=0)
entry_makh = Entry(frame_Info, width=10).grid(row=2, column=1)

label_maphong = Label(
    frame_Info, 
    text="Mã phòng: ", 
    font=("Time news roman",14,"bold"), 
    foreground="#2F4156", background="#E6F2FA").grid(row=3, column=0)
entry_maphong = Entry(frame_Info, width=10).grid(row=3, column=1)

label_madv = Label(
    frame_Info, 
    text="Mã dịch vụ: ", 
    font=("Time news roman",14,"bold"), 
    foreground="#2F4156", background="#E6F2FA").grid(row=0, column=2)
cbb_madv = ttk.Combobox(frame_Info, width=20).grid(row=0, column=3)

label_tienphong = Label(
    frame_Info, text="Tiền phòng: ", 
    font=("Time news roman",14,"bold"), 
    foreground="#2F4156", background="#E6F2FA").grid(row=1, column=2)
entry_tienphong = Entry(frame_Info, width=10).grid(row=1, column=3)

label_tiendv = Label(
    frame_Info, 
    text="Tiền dịch vụ: ", 
    font=("Time news roman",14,"bold"), 
    foreground="#2F4156", background="#E6F2FA").grid(row=2, column=2)
entry_tiendv = Entry(frame_Info, width=10).grid(row=2, column=3)

label_tongtien = Label(
    frame_Info, text="Tổng tiền: ", 
    font=("Time news roman",14,"bold"), 
    foreground="#2F4156", background="#E6F2FA").grid(row=3, column=2)
entry_tongtien = Entry(frame_Info, width=10).grid(row=3, column=3)
frame_Info.pack(pady=50, padx=10, fill="x")
frame_Info.configure(bg="#E6F2FA")

# ===== Frame Button =====
frame_Btn = Frame(hoadon)
Button(frame_Btn, text="Thêm", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=0, padx=5)
Button(frame_Btn, text="Xoá", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=1, padx=5)
Button(frame_Btn, text="Sửa", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=2, padx=5)
Button(frame_Btn, text="Thoát", width=8, command=hoadon.quit,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=5, padx=5)

frame_Btn.pack(pady=5)
frame_Btn.config(bg="#E6F2FA")

# ====== Bảng danh sách hoá đơn ====== MaHoaDon, MaNVThanhToan, MaKH, MaPhong, MaDVDaDat, TienPhong, TienDV, TongTien
frame_Table = Frame(hoadon)
Label(frame_Table, text="Danh sách hoá đơn", font=("Time new roman",14,"bold"), foreground="#2F4156", background="#E6F2FA").pack(pady=5, anchor="w", padx=10)
frame_Table.pack()
frame_Table.configure(background="#E6F2FA")

columns = ("Mã hoá đơn", "Mã NV Thanh toán", "Mã KH", "Mã phòng", "Mã dịch vụ", "Tiền phòng", "Tiền dịch vụ", "Tổng tiền")
tree = ttk.Treeview(frame_Table, columns=columns, show="headings", height=10)
for col in columns:
 tree.heading(col, text=col.capitalize())
tree.column("Mã hoá đơn", width=100, anchor="center")
tree.column("Mã NV Thanh toán", width=100)
tree.column("Mã KH", width=100)
tree.column("Mã phòng", width=100)
tree.column("Mã dịch vụ", width=100)
tree.column("Tiền phòng", width=150)
tree.column("Tiền dịch vụ", width=150)
tree.column("Tổng tiền", width=150)
tree.pack(padx=10, pady=5, fill="both")

hoadon.mainloop()