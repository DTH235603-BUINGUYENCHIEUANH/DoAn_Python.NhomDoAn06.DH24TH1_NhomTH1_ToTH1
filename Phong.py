from tkinter import *
from tkinter import ttk, messagebox
from QLKS import connect_db  # Đảm bảo bạn có hàm connect_db() trả về kết nối MySQL

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
frmPhong = Tk()
frmPhong.title("Phòng khách sạn")
center_window(frmPhong, 700, 500)
frmPhong.configure(bg="#E6F2FA")
frmPhong.resizable(False, False)

# ====== Tiêu đề ======
Label(frmPhong, text="QUẢN LÝ PHÒNG KHÁCH SẠN", font=("Times New Roman", 18, "bold"), bg="#E6F2FA").pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = Frame(frmPhong, bg="#E6F2FA")
frame_info.pack(pady=5, padx=10, fill="x")

Label(frame_info, text="Mã phòng", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_map = Entry(frame_info, width=15)
entry_map.grid(row=0, column=1, padx=5, pady=5)

Label(frame_info, text="Tên phòng", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_tenp = Entry(frame_info, width=15)
entry_tenp.grid(row=0, column=3, padx=5, pady=5)

Label(frame_info, text="Loại phòng", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_loaiphong = Entry(frame_info, width=15)
entry_loaiphong.grid(row=1, column=1, padx=5, pady=5)

Label(frame_info, text="Giá phòng", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_giaphong = Entry(frame_info, width=15)
entry_giaphong.grid(row=1, column=3, padx=5, pady=5)

Label(frame_info, text="Trạng thái", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_trangthai = Entry(frame_info, width=15)
entry_trangthai.grid(row=2, column=1, padx=5, pady=5)

# ====== Bảng danh sách phòng ======
Label(frmPhong, text="Danh sách phòng", font=("Times New Roman", 10, "bold"), bg="#E6F2FA").pack(pady=5, anchor="w", padx=10)

columns = ("Mã phòng", "Tên phòng", "loại phòng", "giá phòng", "trạng thái")
tree = ttk.Treeview(frmPhong, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(padx=10, pady=5, fill="both")


# ====== Chức năng ======
def clear_input():
    entry_map.delete(0, END)
    entry_tenp.delete(0, END)
    entry_loaiphong.delete(0, END)
    entry_giaphong.delete(0, END)
    entry_trangthai.delete(0, END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Phong")
    for row in cur.fetchall():
        tree.insert("", END, values=row)
    conn.close()

def them_phong():
    map = entry_map.get()
    tenp = entry_tenp.get()
    loaiphong = entry_loaiphong.get()
    giaphong = entry_giaphong.get()
    trangthai = entry_trangthai.get()

    if map == "" or tenp == "" or loaiphong == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Phong WHERE map = %s", (map,))
    if cur.fetchone():
        messagebox.showwarning("Trùng mã", "Mã phòng đã tồn tại!")
        conn.close()
        return

    try:
        cur.execute("INSERT INTO Phong VALUES (%s, %s, %s, %s, %s)",
                    (map, tenp, loaiphong, giaphong, trangthai))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def xoa_phong():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn phòng để xóa")
        return
    map = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM Phong WHERE map=%s", (map,))
    conn.commit()
    conn.close()
    load_data()

def sua_phong():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn phòng để sửa")
        return
    values = tree.item(selected)["values"]
    entry_map.delete(0, END)
    entry_map.insert(0, values[0])
    entry_tenp.delete(0, END)
    entry_tenp.insert(0, values[1])
    entry_loaiphong.delete(0, END)
    entry_loaiphong.insert(0, values[2])
    entry_giaphong.delete(0, END)
    entry_giaphong.insert(0, values[3])
    entry_trangthai.delete(0, END)
    entry_trangthai.insert(0, values[4])

def luu_phong():
    map = entry_map.get()
    tenp = entry_tenp.get()
    loaiphong = entry_loaiphong.get()
    giaphong = entry_giaphong.get()
    trangthai = entry_trangthai.get()

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""UPDATE Phong SET tenp=%s, loaiphong=%s, giaphong=%s, trangthai=%s
                   WHERE map=%s""",
                (tenp, loaiphong, giaphong, trangthai, map))
    conn.commit()
    conn.close()
    load_data()
    clear_input()

# ====== Frame nút ======
frame_btn = Frame(frmPhong, bg="#E6F2FA")
frame_btn.pack(pady=5)

Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_phong).grid(row=0, column=0, padx=5)
Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_phong).grid(row=0, column=1, padx=5)
Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_phong).grid(row=0, column=2, padx=5)
Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=3, padx=5)
Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_phong).grid(row=0, column=4, padx=5)
Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmPhong.quit).grid(row=0, column=5, padx=5)

# ====== Khởi động ======

frmPhong.mainloop()