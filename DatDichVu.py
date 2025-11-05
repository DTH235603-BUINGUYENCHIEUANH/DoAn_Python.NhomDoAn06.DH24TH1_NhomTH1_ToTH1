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
frmDatDV = Tk()
frmDatDV.title("Đặt DV khách sạn")
center_window(frmDatDV, 700, 500)
frmDatDV.configure(bg="#E6F2FA")
frmDatDV.resizable(False, False)

# ====== Tiêu đề ======
Label(frmDatDV, text="QUẢN LÝ ĐẶT DỊCH VỤ KHÁCH SẠN", font=("Times New Roman", 18, "bold"), bg="#E6F2FA").pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = Frame(frmDatDV, bg="#E6F2FA")
frame_info.pack(pady=5, padx=10, fill="x")

Label(frame_info, text="Mã đặt DV", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_maddv = Entry(frame_info, width=15)
entry_maddv.grid(row=0, column=1, padx=5, pady=5)

Label(frame_info, text="Mã KH đặt DV", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_makhddv = Entry(frame_info, width=15)
entry_makhddv.grid(row=0, column=3, padx=5, pady=5)

Label(frame_info, text="Mã DV", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_madv = Entry(frame_info, width=15)
entry_madv.grid(row=1, column=1, padx=5, pady=5)

Label(frame_info, text="Số lượng", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_soluongDV = Entry(frame_info, width=15)
entry_soluongDV.grid(row=1, column=3, padx=5, pady=5)

Label(frame_info, text="Thành tiền", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_thanhtien = Entry(frame_info, width=15)
entry_thanhtien.grid(row=2, column=1, padx=5, pady=5)

# ====== Bảng danh sách phòng ======
Label(frmDatDV, text="Danh sách đặt DV", font=("Times New Roman", 10, "bold"), bg="#E6F2FA").pack(pady=5, anchor="w", padx=10)

columns = ("Mã đặt DV", "Mã KH đặt DV", "Mã DV", "Số Lượng DV", "Thành tiền")
tree = ttk.Treeview(frmDatDV, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(padx=10, pady=5, fill="both")


# ====== Chức năng ======
def clear_input():
    entry_maddv.delete(0, END)
    entry_makhddv.delete(0, END)
    entry_madv.delete(0, END)
    entry_soluongDV.delete(0, END)
    entry_thanhtien.delete(0, END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM DatDV")
    for row in cur.fetchall():
        tree.insert("", END, values=row)
    conn.close()

def them_DatDV():
    maddv = entry_maddv.get()
    makhddv = entry_makhddv.get()
    madv = entry_madv.get()
    soluongDV = entry_soluongDV.get()
    thanhtien = entry_thanhtien.get()
    

    if maddv == "" or makhddv == "" or madv == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM DatDV  WHERE map = %s", (maddv,))
    if cur.fetchone():
        messagebox.showwarning("Trùng mã", "Mã đặt DV đã tồn tại!")
        conn.close()
        return

    try:
        cur.execute("INSERT INTO Phong VALUES (%s, %s, %s, %s, %s)",
                    (maddv, makhddv, madv, soluongDV, thanhtien))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def xoa_DatDV():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn dịch vụ để xóa")
        return
    map = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM DatDV WHERE maddv=%s", (maddv,))
    conn.commit()
    conn.close()
    load_data()

def sua_DatDV():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn dịch vụ để sửa")
        return
    values = tree.item(selected)["values"]
    entry_maddv.delete(0, END)
    entry_maddv.insert(0, values[0])
    entry_makhddv.delete(0, END)
    entry_makhddv.insert(0, values[1])
    entry_madv.delete(0, END)
    entry_madv.insert(0, values[2])
    entry_soluongDV.delete(0, END)
    entry_soluongDV.insert(0, values[3])
    entry_thanhtien.delete(0, END)
    entry_thanhtien.insert(0, values[4])
   

def luu_DatDV():
    maddv = entry_maddv.get()
    makhddv = entry_makhddv.get()
    madv = entry_madv.get()
    soluongDV = entry_soluongDV.get()
    thanhtien = entry_thanhtien.get()
    

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""UPDATE DatDV SET makhddv=%s, madv=%s, soluongDV=%s, thanhtien=%s
                   WHERE maddv=%s""",
                (makhddv, madv, soluongDV, thanhtien, maddv))
    conn.commit()
    conn.close()
    load_data()
    clear_input()

# ====== Frame nút ======
frame_btn = Frame(frmDatDV, bg="#E6F2FA")
frame_btn.pack(pady=5)

Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_DatDV).grid(row=0, column=0, padx=5)
Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_DatDV).grid(row=0, column=1, padx=5)
Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_DatDV).grid(row=0, column=2, padx=5)
Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=3, padx=5)
Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_DatDV).grid(row=0, column=4, padx=5)
Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmDatDV.quit).grid(row=0, column=5, padx=5)

# ====== Khởi động ======

frmDatDV.mainloop()