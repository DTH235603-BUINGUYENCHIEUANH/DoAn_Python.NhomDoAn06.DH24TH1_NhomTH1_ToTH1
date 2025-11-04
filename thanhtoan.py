from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import connect_db

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')
    
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
# ====== Thông tin hoá đơn ======
lbl_mahd = Label(frame_Info, text="Mã hoá đơn", font=("Times New Roman", 14, "bold"), foreground="#2F4156", background="#E6F2FA")
lbl_mahd.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_mahd = Entry(frame_Info, width=15)
entry_mahd.grid(row=0, column=1, padx=5, pady=5, sticky="w")

lbl_manvtt = Label(frame_Info, text="Mã nhân viên thanh toán", font=("Times New Roman", 14, "bold"), foreground="#2F4156", background="#E6F2FA")
lbl_manvtt.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_manvtt = Entry(frame_Info, width=15)
entry_manvtt.grid(row=1, column=1, padx=5, pady=5, sticky="w")

lbl_makh = Label(frame_Info, text="Mã khách hàng", font=("Times New Roman", 14, "bold"), foreground="#2F4156", background="#E6F2FA")
lbl_makh.grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_makh = Entry(frame_Info, width=15)
entry_makh.grid(row=0, column=3, padx=5, pady=5, sticky="w")

lbl_phuongthuctt = Label(frame_Info, text="Phương thức thanh toán", font=("Times New Roman", 14, "bold"),foreground="#2F4156", background="#E6F2FA")
lbl_phuongthuctt.grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_phuongthuctt = Entry(frame_Info, width=15)
entry_phuongthuctt.grid(row=1, column=3, padx=5, pady=5, sticky="w")

lbl_tongtien = Label(frame_Info, text="Tổng tiền", font=("Times New Roman", 14, "bold"),foreground="#2F4156", background="#E6F2FA")
lbl_tongtien.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_tongtien = Entry(frame_Info, width=15)
entry_tongtien.grid(row=2, column=1, padx=5, pady=5, sticky="w")

frame_Info.pack(pady=50, padx=10, fill="x")
frame_Info.configure(bg="#E6F2FA")

# ===== Frame Button =====
frame_Btn = Frame(hoadon)
Button(frame_Btn, text="Thêm", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=0, padx=5)
Button(frame_Btn, text="Xoá", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=1, padx=5)
Button(frame_Btn, text="Sửa", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=2, padx=5)
Button(frame_Btn, text="Lưu", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=3, padx=5)
Button(frame_Btn, text="Thoát", width=8, command=hoadon.quit,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=5, padx=5)
frame_Btn.pack(pady=5)
frame_Btn.config(bg="#E6F2FA")

# ====== Bảng danh sách hoá đơn ====== MaHoaDon, MaNVThanhToan, MaKH, MaPhong, MaDVDaDat, TienPhong, TienDV, TongTien
frame_Table = Frame(hoadon)
Label(frame_Table, text="Danh sách hoá đơn", font=("Time new roman",14,"bold"), foreground="#2F4156", background="#E6F2FA").pack(pady=5, anchor="w", padx=10)
frame_Table.pack()
frame_Table.configure(background="#E6F2FA")

columns = ("Mã hoá đơn", "Mã NV Thanh toán", "Mã KH", "Phương thức thanh toán", "Tổng tiền")
tree = ttk.Treeview(frame_Table, columns=columns, show="headings", height=10)
for col in columns:
 tree.heading(col, text=col.capitalize())
tree.column("Mã hoá đơn", width=100, anchor="center")
tree.column("Mã NV Thanh toán", width=100)
tree.column("Mã KH", width=100)
tree.column("Phương thức thanh toán", width=150)
tree.column("Tổng tiền", width=100)
tree.pack(padx=10, pady=5, fill="both")

hoadon.mainloop()