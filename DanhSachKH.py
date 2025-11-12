from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur  
from Menu import create_menu

def open_form_DanhSachKH(vaitro):

    # ====== Hàm canh giữa cửa sổ ======
    def center_window(win, w=800, h=600):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    # ====== Cửa sổ chính ======
    frmKhachHang = Tk()
    frmKhachHang.title("Quản lý khách hàng")
    frmKhachHang.minsize(width=800, height=600)
    center_window(frmKhachHang)
    frmKhachHang.configure(bg="#E6F2FA")
    frmKhachHang.resizable(False, False)

    # ===== Hiển thị menu =====
    create_menu(frmKhachHang, "DanhSachKH", vaitro)

    # ====== Tiêu đề ======
    lbl_title = Label(frmKhachHang, text="QUẢN LÝ KHÁCH HÀNG", foreground="#2F4156", font=("Times New Roman", 18, "bold"), bg="#E6F2FA")
    lbl_title.pack(pady=10)

    # ====== Frame nhập thông tin ======
    frame_info = Frame(frmKhachHang, bg="#E6F2FA")
    frame_info.pack(pady=5, padx=10)

    Label(frame_info, text="Mã KH", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_makh = Entry(frame_info, width=15)
    entry_makh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Họ tên KH", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_hoten = Entry(frame_info, width=25)
    entry_hoten.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Quốc tịch", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_quoctich = Entry(frame_info, width=15)
    entry_quoctich.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    Label(frame_info, text="SĐT", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_sdt = Entry(frame_info, width=15)
    entry_sdt.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="CCCD", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_cccd = Entry(frame_info, width=15)
    entry_cccd.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Email", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=3, column=0, padx=5, pady=5, sticky="w")
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
    frame_table = Frame(frmKhachHang, bg="#E6F2FA", bd=2, relief="groove")
    frame_table.pack(pady=5, expand=True)

    columns = ("Mã khách hàng", "Họ tên KH", "Quốc tịch", "Số điện thoại", "CCCD", "Email") 
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)

    # ====== Thanh cuộn ======
    scroll_y = Scrollbar(frame_table, orient="vertical", command=tree.yview, bg="#E6F2FA")
    scroll_x = Scrollbar(frame_table, orient="horizontal", command=tree.xview, bg="#E6F2FA")
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # ====== Đặt vị trí ======
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(side="left", fill="both", expand=True)

    for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
    
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

    btn_Them = Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_khachang)
    btn_Them.grid(row=0, column=0, padx=5)
    btn_Xoa = Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_khachhang)
    btn_Xoa.grid(row=0, column=1, padx=5)
    btn_Sua = Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_khachhang)
    btn_Sua.grid(row=0, column=2, padx=5)
    btn_Luu = Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_khachhang)
    btn_Luu.grid(row=0, column=3, padx=5)
    btn_Huy = Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input)
    btn_Huy.grid(row=0, column=4, padx=5)
    btn_Refresh = Button(frame_btn, text="Refresh", width=8, bg="#00AEEF", fg="white", command=load_data)
    btn_Refresh.grid(row=0, column=5, padx=5)
    btn_Thoat = Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmKhachHang.quit)
    btn_Thoat.grid(row=0, column=6, padx=5)

    # ===== Phân quyền =====
    if vaitro.lower() == 'user':  # Nếu là User, vô hiệu hoá nút thao tác (Trừ nút thoát)
        btn_Them.config(state=DISABLED, bg="gray")
        btn_Xoa.config(state=DISABLED, bg="gray")
        btn_Sua.config(state=DISABLED, bg="gray")
        btn_Luu.config(state=DISABLED, bg="gray")
        btn_Huy.config(state=DISABLED, bg="gray")
        btn_Refresh.config(state=DISABLED, bg="gray")
    
    load_data()
    frmKhachHang.mainloop()