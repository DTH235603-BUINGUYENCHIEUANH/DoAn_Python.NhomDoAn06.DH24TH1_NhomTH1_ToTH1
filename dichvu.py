from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import connect_db

# ===== Cửa sổ chính =====
dichvu = Tk()
dichvu.title("Dịch vụ - Quản lý khách sạn")
dichvu.minsize(width=400, height=400)
dichvu.configure(bg="#E6F2FA")

# ==== Title ====
frame_Title = Frame(dichvu)
Label(frame_Title, text="HỆ THỐNG DỊCH VỤ KHÁCH SẠN TOM AND JERRY", font=("Time news roman",20, "bold"), foreground="#2F4156", background="#E6F2FA").pack()
frame_Title.pack(pady=10, padx=10, fill="x", anchor=CENTER)
frame_Title.configure(bg="#E6F2FA")

# ==== Frame nhập thông tin ==== 
frame_Info = Frame(dichvu)
Label(frame_Info, text="Mã dịch vụ: ", font=("Time news roman",14,"bold"), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=0)
Entry(frame_Info, width=10).grid(row=0, column=1)

Label(frame_Info, text="Tên dịch vụ: ", font=("Time news roman",14,"bold"), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=2)
Entry(frame_Info, width=20).grid(row=0, column=3)

Label(frame_Info, text="Giá dịch vụ: ", font=("Time news roman",14,"bold"), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=4)
Entry(frame_Info, width=10).grid(row=0, column=5)
frame_Info.pack(pady=5, padx=10, fill="x")
frame_Info.configure(bg="#E6F2FA")

# ===== Frame Button =====
frame_Btn = Frame(dichvu)
Button(frame_Btn, text="Thêm", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=0, padx=5)
Button(frame_Btn, text="Xoá", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=1, padx=5)
Button(frame_Btn, text="Sửa", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=2, padx=5)
Button(frame_Btn, text="Thoát", width=8, command=dichvu.quit,  font=("Time news roman",10), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=5, padx=5)
frame_Btn.pack(pady=5)
frame_Btn.config(bg="#E6F2FA")

# ====== Bảng danh sách dịch vụ ======
frame_Table = Frame(dichvu)
Label(frame_Table, text="Danh sách dịch vụ", font=("Time new roman",14,"bold"), foreground="#2F4156", background="#E6F2FA").pack(pady=5, anchor="w", padx=10)
frame_Table.pack()
frame_Table.configure(background="#E6F2FA")

columns = ("Mã dịch vụ", "Tên dịch vụ", "Giá dịch vụ")
tree = ttk.Treeview(frame_Table, columns=columns, show="headings", height=10)
for col in columns:
 tree.heading(col, text=col.capitalize())
tree.column("Mã dịch vụ", width=100, anchor="center")
tree.column("Tên dịch vụ", width=200)
tree.column("Giá dịch vụ", width=100)
tree.pack(padx=10, pady=5, fill="both")

dichvu.mainloop()

