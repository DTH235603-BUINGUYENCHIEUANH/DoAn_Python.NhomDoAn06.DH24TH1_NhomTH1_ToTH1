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
entry_Madv = Entry(frame_Info, width=10)
entry_Madv .grid(row=0, column=1)

Label(frame_Info, text="Tên dịch vụ: ", font=("Time news roman",14,"bold"), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=2)
entry_Tendv = Entry(frame_Info, width=20)
entry_Tendv.grid(row=0, column=3)

Label(frame_Info, text="Giá dịch vụ: ", font=("Time news roman",14,"bold"), foreground="#2F4156", background="#E6F2FA").grid(row=0, column=4)
entry_GiaDV = Entry(frame_Info, width=10)
entry_GiaDV.grid(row=0, column=5)
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

