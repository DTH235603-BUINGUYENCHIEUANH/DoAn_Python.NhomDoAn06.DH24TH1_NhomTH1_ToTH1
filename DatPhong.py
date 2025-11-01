import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# ====== Kết nối MySQL ======


# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
frmDatPhong = tk.Tk()
frmDatPhong.title("Quản lý đặt phòng")
center_window(frmDatPhong, 700, 500)
frmDatPhong.configure(bg="#E6F2FA")
frmDatPhong.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = tk.Label(frmDatPhong, text="QUẢN LÝ ĐẶT PHÒNG", font=("Times New Roman", 18, "bold"), bg="#E6F2FA")
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(frmDatPhong, bg="#E6F2FA")
frame_info.pack(pady=5, padx=10, fill="x")

tk.Label(frame_info, text="Mã đặt phòng", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_madp = tk.Entry(frame_info, width=15)
entry_madp.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Mã khách hàng", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_makh = tk.Entry(frame_info, width=15)
entry_makh.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Mã phòng", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_maphong = tk.Entry(frame_info, width=15)
entry_maphong.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Ngày đặt", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
date_ngaydat = DateEntry(frame_info, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
date_ngaydat.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Ngày trả", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
date_ngaytra = DateEntry(frame_info, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
date_ngaytra.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Số lượng khách", bg="#E6F2FA").grid(row=2, column=2, padx=5, pady=5, sticky="w")
entry_soluong = tk.Entry(frame_info, width=10)
entry_soluong.grid(row=2, column=3, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Ghi chú", bg="#E6F2FA").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_ghichu = tk.Entry(frame_info, width=50)
entry_ghichu.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")

# ====== Bảng danh sách đặt phòng ======
lbl_ds = tk.Label(frmDatPhong, text="Danh sách đặt phòng", font=("Times New Roman", 10, "bold"), bg="#E6F2FA")
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("Mã đặt phòng", "Mã KH", "Mã phòng", "Ngày đặt", "Ngày trả", "Số lượng", "Ghi chú")
tree = ttk.Treeview(frmDatPhong, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.pack(padx=10, pady=5, fill="both")

# Độ rộng cột và căn lề từng cột
tree.column("Mã đặt phòng", width=120, anchor="center")
tree.column("Mã KH", width=120, anchor="center")
tree.column("Mã phòng", width=100, anchor="center")
tree.column("Ngày đặt", width=100, anchor="center")
tree.column("Ngày trả", width=100, anchor="center")
tree.column("Số lượng", width=130, anchor="center")
tree.column("Ghi chú", width=200, anchor="w")


# ====== Chức năng ======
def clear_input():
    entry_madp.delete(0, tk.END)
    entry_makh.delete(0, tk.END)
    entry_maphong.delete(0, tk.END)
    date_ngaydat.set_date("2025-01-01")
    date_ngaytra.set_date("2025-01-02")
    entry_soluong.delete(0, tk.END)
    entry_ghichu.delete(0, tk.END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM datphong")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def them_datphong():
    madp = entry_madp.get()
    makh = entry_makh.get()
    maphong = entry_maphong.get()
    ngaydat = date_ngaydat.get()
    ngaytra = date_ngaytra.get()
    soluong = entry_soluong.get()
    ghichu = entry_ghichu.get()
    if madp == "" or makh == "" or maphong == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO datphong VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (madp, makh, maphong, ngaydat, ngaytra, soluong, ghichu))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def xoa_datphong():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn đặt phòng để xóa")
        return
    madp = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM datphong WHERE madatphong=%s", (madp,))
    conn.commit()
    conn.close()
    load_data()

def sua_datphong():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn đặt phòng để sửa")
        return
    values = tree.item(selected)["values"]
    entry_madp.delete(0, tk.END)
    entry_madp.insert(0, values[0])
    entry_makh.delete(0, tk.END)
    entry_makh.insert(0, values[1])
    entry_maphong.delete(0, tk.END)
    entry_maphong.insert(0, values[2])
    date_ngaydat.set_date(values[3])
    date_ngaytra.set_date(values[4])
    entry_soluong.delete(0, tk.END)
    entry_soluong.insert(0, values[5])
    entry_ghichu.delete(0, tk.END)
    entry_ghichu.insert(0, values[6])

def luu_datphong():
    madp = entry_madp.get()
    makh = entry_makh.get()
    maphong = entry_maphong.get()
    ngaydat = date_ngaydat.get()
    ngaytra = date_ngaytra.get()
    soluong = entry_soluong.get()
    ghichu = entry_ghichu.get()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""UPDATE datphong SET makh=%s, maphong=%s, ngaydat=%s, ngaytra=%s, soluongkhach=%s, ghichu=%s
                WHERE madatphong=%s""",
                (makh, maphong, ngaydat, ngaytra, soluong, ghichu, madp))
    conn.commit()
    conn.close()
    load_data()
    clear_input()

# ====== Frame nút ======
frame_btn = tk.Frame(frmDatPhong, bg="#E6F2FA")
frame_btn.pack(pady=5)


tk.Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_datphong).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_datphong).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_datphong).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_datphong).grid(row=0, column=4, padx=5)
tk.Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmDatPhong.quit).grid(row=0, column=5, padx=5)

# ====== Chạy giao diện ======
frmDatPhong.mainloop()