from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur  

def open_form_khachhang():

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

    Label(frame_info, text="CCCD", bg="#E6F2FA").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_cccd = Entry(frame_info, width=15)
    entry_cccd.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Email", bg="#E6F2FA").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_email = Entry(frame_info, width=40)
    entry_email.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")

    # Load
    def load_data():
        if conn is None or cur is None:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
            return
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM KHACHHANG")
        for row in cur.fetchall():
            tree.insert("", END, values=row)


    # ====== Bảng danh sách khách hàng ======
    lbl_ds = Label(frmKhachHang, text="Danh sách khách hàng", font=("Times New Roman", 10, "bold"), bg="#E6F2FA")
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    columns = ("MaKH", "HoTenKH", "QuocTich", "Sdt", "CCCD", "Email") 
    tree = ttk.Treeview(frmKhachHang, columns=columns, show="headings", height=10)
    tree.heading("MaKH", text="Mã KH")
    tree.heading("HoTenKH", text="Họ tên KH")
    tree.heading("QuocTich", text="Quốc tịch")
    tree.heading("Sdt", text="SĐT")
    tree.heading("CCCD", text="CCCD")
    tree.heading("Email", text="Email")

    tree.column("MaKH", width=100, anchor="center")
    tree.column("HoTenKH", width=150)
    tree.column("QuocTich", width=100, anchor="center")
    tree.column("Sdt", width=100, anchor="center")
    tree.column("CCCD", width=100, anchor="center")
    tree.column("Email", width=200)
    tree.pack(padx=10, pady=5, fill="both")
    load_data()

    # ====== Chức năng ======
    # ===== Hàm xử lý =====

    # Clear
    def clear_input():
        entry_makh.delete(0, END)
        entry_hoten.delete(0, END)
        entry_quoctich.delete(0, END)
        entry_sdt.delete(0, END)
        entry_cccd.delete(0, END)
        entry_email.delete(0, END)

    # Thêm
    def them_khachang():
        makh = entry_makh.get().strip() 
        hoten = entry_hoten.get().strip()
        quoctich = entry_quoctich.get().strip()
        sdt = entry_sdt.get().strip()
        cccd = entry_cccd.get().strip()
        email = entry_email.get().strip()
        if not makh or not hoten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            # Kiểm tra xem MaKH đã tồn tại chưa
            cur.execute("SELECT COUNT(*) FROM KHACHHANG WHERE MaKH = %s", (makh,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Trùng lặp", f"Mã khách hàng '{makh}' đã tồn tại. Vui lòng chọn mã khác.")
                return
            # Sửa: Loại bỏ quoctich lặp lại
            cur.execute("INSERT INTO KHACHHANG (MaKH, HoTenKH, QuocTich, Sdt, CCCD, Email) VALUES (%s,%s,%s,%s,%s,%s)", (makh, hoten, quoctich, sdt, cccd, email))
            conn.commit()
            load_data() 
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm khách hàng mới.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm: {e}")

    #Xoá
    def xoa_khachhang():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để xóa.")
            return
        makh = tree.item(selected)["values"][0]
        #Xác nhận trước khi xoá
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng '{makh}'?")
        if not confirm:
            return
        try:
            # Sửa: Tên bảng đúng
            cur.execute("DELETE FROM KHACHHANG WHERE MaKH=%s", (makh,))
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Đã xóa", f"Khách hàng {makh} đã được xóa.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa: {e}")

    # Sửa
    def sua_khachhang():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa.")
            return
        values = tree.item(selected)["values"]
        entry_makh.delete(0, END), entry_makh.insert(0, values[0])
        entry_makh.config(state='disabled')  # Thêm dòng này để khóa MaDV
        entry_hoten.delete(0, END), entry_hoten.insert(0, values[1])
        entry_quoctich.delete(0, END), entry_quoctich.insert(0, values[2])
        entry_sdt.delete(0, END), entry_sdt.insert(0, values[3])
        entry_cccd.delete(0, END), entry_cccd.insert(0, values[4])
        entry_email.delete(0, END), entry_email.insert(0, values[5])

    # Lưu 
    def luu_khachhang():
        makh = entry_makh.get()
        hoten = entry_hoten.get()
        quoctich = entry_quoctich.get()
        sdt = entry_sdt.get()
        cccd = entry_cccd.get()
        email = entry_email.get()

        if not makh or not hoten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return    
        try:
            cur.execute("UPDATE KHACHHANG SET HoTenKH=%s, QuocTich=%s, Sdt=%s, CCCD=%s, Email=%s WHERE MaKH=%s", (hoten, quoctich, sdt, cccd, email, makh))
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")
        entry_makh.config(state='normal')  # Mở khóa sau khi lưu

    # ====== Frame nút ======
    frame_btn = Frame(frmKhachHang, bg="#E6F2FA")
    frame_btn.pack(pady=5)

    Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_khachang).grid(row=0, column=0, padx=5)
    Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_khachhang).grid(row=0, column=1, padx=5)
    Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_khachhang).grid(row=0, column=2, padx=5)
    Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=3, padx=5)
    Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_khachhang).grid(row=0, column=4, padx=5)
    
    load_data()
    frmKhachHang.mainloop()