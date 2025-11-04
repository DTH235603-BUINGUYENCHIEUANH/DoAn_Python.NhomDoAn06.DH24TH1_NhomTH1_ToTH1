from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from QLKS import connect_db
import mysql.connector

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="qlks"
    )

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
frmKhachHang = Tk()
frmKhachHang.title("Quản lý khách hàng")
center_window(frmKhachHang, 700, 500)
frmKhachHang.configure(bg="#E6F2FA")
frmKhachHang.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = Label(frmKhachHang, text="QUẢN LÝ KHÁCH HÀNG", font=("Times New Roman", 18, "bold"), bg="#E6F2FA")
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = Frame(frmKhachHang, bg="#E6F2FA")
frame_info.pack(pady=5, padx=10, fill="x")

Label(frame_info, text="Mã KH", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_makh = Entry(frame_info, width=15)
entry_makh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

Label(frame_info, text="Họ tên KH", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_hoten = Entry(frame_info, width=25)
entry_hoten.grid(row=0, column=3, padx=5, pady=5, sticky="w")

Label(frame_info, text="Quốc tịch", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_quoctich = Entry(frame_info, width=15)
entry_quoctich.grid(row=1, column=1, padx=5, pady=5, sticky="w")

Label(frame_info, text="SĐT", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_sdt = Entry(frame_info, width=15)
entry_sdt.grid(row=1, column=3, padx=5, pady=5, sticky="w")

Label(frame_info, text="Email", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_email = Entry(frame_info, width=40)
entry_email.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")

# ====== Bảng danh sách khách hàng ======
lbl_ds = Label(frmKhachHang, text="Danh sách khách hàng", font=("Times New Roman", 10, "bold"), bg="#E6F2FA")
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("MaKH", "HoTenKH", "QuocTich", "Sdt", "Email")
tree = ttk.Treeview(frmKhachHang, columns=columns, show="headings", height=10)
tree.heading("MaKH", text="Mã KH")
tree.heading("HoTenKH", text="Họ tên KH")
tree.heading("QuocTich", text="Quốc tịch")
tree.heading("Sdt", text="SĐT")
tree.heading("Email", text="Email")

tree.column("MaKH", width=100, anchor="center")
tree.column("HoTenKH", width=150)
tree.column("QuocTich", width=100, anchor="center")
tree.column("Sdt", width=100, anchor="center")
tree.column("Email", width=200)
tree.pack(padx=10, pady=5, fill="both")

# ====== Chức năng ======
def clear_input():
    entry_makh.delete(0, END)
    entry_hoten.delete(0, END)
    entry_quoctich.delete(0, END)
    entry_sdt.delete(0, END)
    entry_email.delete(0, END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM khachhang")
    for row in cur.fetchall():
        tree.insert("", END, values=row)
    conn.close()

def them_khachhang():
    makh = entry_makh.get()
    hoten = entry_hoten.get()
    quoctich = entry_quoctich.get()
    sdt = entry_sdt.get()
    email = entry_email.get()
    if makh == "" or hoten == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO khachhang VALUES (%s, %s, %s, %s, %s)", (makh, hoten, quoctich, sdt, email))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def xoa_khachhang():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn khách hàng để xóa")
        return
    makh = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM khachhang WHERE MaKH=%s", (makh,))
    conn.commit()
    conn.close()
    load_data()

def sua_khachhang():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn khách hàng để sửa")
        return
    values = tree.item(selected)["values"]
    entry_makh.delete(0, END)
    entry_makh.insert(0, values[0])
    entry_hoten.delete(0, END)
    entry_hoten.insert(0, values[1])
    entry_quoctich.delete(0, END)
    entry_quoctich.insert(0, values[2])
    entry_sdt.delete(0, END)
    entry_sdt.insert(0, values[3])
    entry_email.delete(0, END)
    entry_email.insert(0, values[4])

def luu_khachhang():
    makh = entry_makh.get()
    hoten = entry_hoten.get()
    quoctich = entry_quoctich.get()
    sdt = entry_sdt.get()
    email = entry_email.get()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""UPDATE khachhang SET HoTenKH=%s, QuocTich=%s, Sdt=%s, Email=%s WHERE MaKH=%s""",
                (hoten, quoctich, sdt, email, makh))
    conn.commit()
    conn.close()
    load_data()
    clear_input()

# ====== Frame nút ======
frame_btn = Frame(frmKhachHang, bg="#E6F2FA")
frame_btn.pack(pady=5)

Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_khachhang).grid(row=0, column=0, padx=5)
Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_khachhang).grid(row=0, column=1, padx=5)
Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_khachhang).grid(row=0, column=2, padx=5)
Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=3, padx=5)
Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_khachhang).grid(row=0, column=4, padx=5)
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="qlks"
    )

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
frmKhachHang = tk.Tk()
frmKhachHang.title("Quản lý khách hàng")
center_window(frmKhachHang, 700, 500)
frmKhachHang.configure(bg="#E6F2FA")
frmKhachHang.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = tk.Label(frmKhachHang, text="QUẢN LÝ KHÁCH HÀNG", font=("Times New Roman", 18, "bold"), bg="#E6F2FA")
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(frmKhachHang, bg="#E6F2FA")
frame_info.pack(pady=5, padx=10, fill="x")

tk.Label(frame_info, text="Mã KH", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_makh = tk.Entry(frame_info, width=15)
entry_makh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Họ tên KH", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_hoten = tk.Entry(frame_info, width=25)
entry_hoten.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Quốc tịch", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_quoctich = tk.Entry(frame_info, width=15)
entry_quoctich.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="SĐT", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_sdt = tk.Entry(frame_info, width=15)
entry_sdt.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Email", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_email = tk.Entry(frame_info, width=40)
entry_email.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")

# ====== Bảng danh sách khách hàng ======
lbl_ds = tk.Label(frmKhachHang, text="Danh sách khách hàng", font=("Times New Roman", 10, "bold"), bg="#E6F2FA")
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("MaKH", "HoTenKH", "QuocTich", "Sdt", "Email")
tree = ttk.Treeview(frmKhachHang, columns=columns, show="headings", height=10)
tree.heading("MaKH", text="Mã KH")
tree.heading("HoTenKH", text="Họ tên KH")
tree.heading("QuocTich", text="Quốc tịch")
tree.heading("Sdt", text="SĐT")
tree.heading("Email", text="Email")

tree.column("MaKH", width=100, anchor="center")
tree.column("HoTenKH", width=150)
tree.column("QuocTich", width=100, anchor="center")
tree.column("Sdt", width=100, anchor="center")
tree.column("Email", width=200)
tree.pack(padx=10, pady=5, fill="both")

# ====== Chức năng ======
def clear_input():
    entry_makh.delete(0, tk.END)
    entry_hoten.delete(0, tk.END)
    entry_quoctich.delete(0, tk.END)
    entry_sdt.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM khachhang")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def them_khachhang():
    makh = entry_makh.get()
    hoten = entry_hoten.get()
    quoctich = entry_quoctich.get()
    sdt = entry_sdt.get()
    email = entry_email.get()
    if makh == "" or hoten == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO khachhang VALUES (%s, %s, %s, %s, %s)", (makh, hoten, quoctich, sdt, email))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def xoa_khachhang():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn khách hàng để xóa")
        return
    makh = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM khachhang WHERE MaKH=%s", (makh,))
    conn.commit()
    conn.close()
    load_data()

def sua_khachhang():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn khách hàng để sửa")
        return
    values = tree.item(selected)["values"]
    entry_makh.delete(0, tk.END)
    entry_makh.insert(0, values[0])
    entry_hoten.delete(0, tk.END)
    entry_hoten.insert(0, values[1])
    entry_quoctich.delete(0, tk.END)
    entry_quoctich.insert(0, values[2])
    entry_sdt.delete(0, tk.END)
    entry_sdt.insert(0, values[3])
    entry_email.delete(0, tk.END)
    entry_email.insert(0, values[4])

def luu_khachhang():
    makh = entry_makh.get()
    hoten = entry_hoten.get()
    quoctich = entry_quoctich.get()
    sdt = entry_sdt.get()
    email = entry_email.get()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""UPDATE khachhang SET HoTenKH=%s, QuocTich=%s, Sdt=%s, Email=%s WHERE MaKH=%s""",
                (hoten, quoctich, sdt, email, makh))
    conn.commit()
    conn.close()
    load_data()
    clear_input()

# ====== Frame nút ======
frame_btn = tk.Frame(frmKhachHang, bg="#E6F2FA")
frame_btn.pack(pady=5)

tk.Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_khachhang).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_khachhang).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_khachhang).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_khachhang).grid(row=0, column=4, padx=5)
tk.Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmKhachHang.quit).grid(row=0, column=5, padx=5)

# ====== Chạy giao diện ======
frmKhachHang.mainloop()