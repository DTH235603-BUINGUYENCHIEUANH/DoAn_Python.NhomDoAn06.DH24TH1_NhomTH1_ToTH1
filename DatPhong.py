from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from QLKS import conn, cur
from Menu import create_menu

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=800, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

def open_form_DatPhong(vaitro):
    frmDatPhong = Tk()
    frmDatPhong.title("Quản lý đặt phòng")
    frmDatPhong.minsize(width=800, height=600)
    center_window(frmDatPhong)
    frmDatPhong.configure(bg="#E6F2FA")
    frmDatPhong.resizable(False, False)

    # ===== Hiển thị menu =====
    create_menu(frmDatPhong, "DatPhong", vaitro)

    Label(frmDatPhong, text="QUẢN LÝ ĐẶT PHÒNG", font=("Times New Roman", 18, "bold"), bg="#E6F2FA").pack(pady=10)

    # ===== Frame nhập thông tin =====
    frame_info = Frame(frmDatPhong, bg="#E6F2FA")
    frame_info.pack(anchor="center", pady=10)

    # Hàng 0
    Label(frame_info, text="Mã đặt phòng", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_madp = Entry(frame_info, width=12)
    entry_madp.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Mã khách hàng", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_makh = Entry(frame_info, width=12)
    entry_makh.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Tên phòng", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    cb_tenphong = ttk.Combobox(frame_info, width=15, state="readonly")
    cb_tenphong.grid(row=0, column=5, padx=5, pady=5, sticky="w")

    # Hàng 1
    Label(frame_info, text="Mã phòng", font=("Times New Roman", 14, "bold"),
          foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_maphong = Entry(frame_info, width=12)
    entry_maphong.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Ngày đặt", font=("Times New Roman", 14, "bold"),
          foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    date_ngaydat = DateEntry(frame_info, date_pattern="yyyy-mm-dd", width=10)
    date_ngaydat.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Ngày trả", font=("Times New Roman", 14, "bold"),
          foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=4, padx=5, pady=5, sticky="e")
    date_ngaytra = DateEntry(frame_info, date_pattern="yyyy-mm-dd", width=10)
    date_ngaytra.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    # Hàng 2
    Label(frame_info, text="Số ngày ở", font=("Times New Roman", 14, "bold"),
          foreground="#2F4156", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_songayo = Entry(frame_info, width=12)
    entry_songayo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Số lượng khách", font=("Times New Roman", 14, "bold"),
          foreground="#2F4156", bg="#E6F2FA").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    entry_soluong = Entry(frame_info, width=12)
    entry_soluong.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Mã KH khác", font=("Times New Roman", 14, "bold"),
          foreground="#2F4156", bg="#E6F2FA").grid(row=2, column=4, padx=5, pady=5, sticky="e")
    entry_makhkhac = Entry(frame_info, width=12)
    entry_makhkhac.grid(row=2, column=5, padx=5, pady=5, sticky="w")

    # Hàng 3
    Label(frame_info, text="Thành tiền", font=("Times New Roman", 14, "bold"),
          foreground="#2F4156", bg="#E6F2FA").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_thanhtien = Entry(frame_info, width=12)
    entry_thanhtien.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Ghi chú", font=("Times New Roman", 14, "bold"),
          foreground="#2F4156", bg="#E6F2FA").grid(row=3, column=2, padx=5, pady=5, sticky="e")
    entry_ghichu = Entry(frame_info, width=40)
    entry_ghichu.grid(row=3, column=3, columnspan=3, padx=5, pady=5, sticky="w")

    # ===== Căn cột đều nhau =====
    for i in range(6):
        frame_info.grid_columnconfigure(i, weight=1, uniform="col")

    # ===== Chức năng tìm kiếm ===== (Pack trước Treeview để tránh bị che)
    frame_TimKiem = Frame(frmDatPhong, bg="#E6F2FA")  
    frame_TimKiem.pack(anchor="center", pady=5)

    # Tiêu đề căn giữa toàn dòng
    Label(frame_TimKiem, text="Tìm kiếm theo mã khách hàng", font=("Times New Roman", 14, "bold"), bg="#E6F2FA").grid(row=0, column=0, columnspan=3, pady=(0, 15))

    # Nhãn + Entry + Nút
    Label(frame_TimKiem, text="Nhập mã KH", font=("Times New Roman", 11, "bold"), bg="#E6F2FA").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_nhapthongtin_timkiem = Entry(frame_TimKiem, width=20)
    entry_nhapthongtin_timkiem.grid(row=1, column=1, padx=10, pady=5)

    # Chia đều độ rộng các cột trong frame_TimKiem để mọi thứ căn giữa
    frame_TimKiem.grid_columnconfigure(0, weight=1, uniform="col")
    frame_TimKiem.grid_columnconfigure(1, weight=1, uniform="col")
    frame_TimKiem.grid_columnconfigure(2, weight=1, uniform="col")

    # ===== Treeview ===== (Pack sau frame_TimKiem)
    # ===== Frame chứa bảng =====
    frame_table = Frame(frmDatPhong, bg="#E6F2FA", bd=2, relief="groove")
    frame_table.pack(pady=5, expand=True)

    columns = ("MaDatPhong","MaKHDatPhong","MaPhong","NgayDat","NgayTra","SoNgayO","SoLuongKhach","MaKHKhac","ThanhTien","GhiChu")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)

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
        tree.column(col, width=100, anchor="center")
    tree.pack(padx=10, pady=10, fill="x")

    # ===== Hàm xử lý =====
    # Hàm tính số ngày ở và thành tiền tự động
    def tinh_songayo_va_thanhtien():
        try:
            ngay_dat = date_ngaydat.get_date()
            ngay_tra = date_ngaytra.get_date()
            if ngay_tra <= ngay_dat:
                messagebox.showwarning("Lỗi", "Ngày trả phải sau ngày đặt.")
                return None, None
            songayo = (ngay_tra - ngay_dat).days
            maphong = entry_maphong.get()
            cur.execute("SELECT Gia FROM PHONG WHERE MaPhong = %s", (maphong,))
            result = cur.fetchone()
            if not result:
                messagebox.showwarning("Lỗi", f"Không tìm thấy phòng {maphong}.")
                return None, None
            gia = float(result[0])
            thanhtien = songayo * gia
            return songayo, thanhtien
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tính toán: {str(e)}")
            return None, None

    def load_phong_to_combobox():
        try:
            cur.execute("SELECT MaPhong, TenPhong FROM PHONG")
            phong_data = cur.fetchall()
            ten_phong_list = [row[1] for row in phong_data]
            cb_tenphong["values"] = ten_phong_list
            # Lưu dict để tra ngược Tên -> Mã
            cb_tenphong.phong_dict = {row[1]: row[0] for row in phong_data}
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi load phòng: {str(e)}")

    def on_select_phong(event):
        ten_phong = cb_tenphong.get()
        if ten_phong in cb_tenphong.phong_dict:
            entry_maphong.delete(0, END)
            entry_maphong.insert(0, cb_tenphong.phong_dict[ten_phong])

    cb_tenphong.bind("<<ComboboxSelected>>", on_select_phong)

    # Clear
    def clear_input():
        entry_madp.delete(0, END)
        entry_makh.delete(0, END)
        entry_maphong.delete(0, END)
        entry_songayo.delete(0, END)
        entry_soluong.delete(0, END)
        entry_makhkhac.delete(0, END)
        entry_thanhtien.delete(0, END)
        entry_ghichu.delete(0, END)
        date_ngaydat.set_date("2025-01-01")
        date_ngaytra.set_date("2025-01-02")

    # Load
    def load_data():
        if conn is None or cur is None:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
            return
        tree.delete(*tree.get_children())
        try:
            cur.execute("SELECT * FROM DATPHONG")
            for row in cur.fetchall():  
                tree.insert("", END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {str(e)}")
    
    # Thêm
    def them_datphong():
        madp = entry_madp.get()
        makh = entry_makh.get()
        maphong = entry_maphong.get()
        ngaydat = date_ngaydat.get_date()
        ngaytra = date_ngaytra.get_date()
        soluong = entry_soluong.get()
        makhkhac = entry_makhkhac.get()
        ghichu = entry_ghichu.get()
        
        if not madp or not makh or not maphong:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ Mã đặt phòng, Mã KH, Mã phòng.")
            return
        
        songayo, thanhtien = tinh_songayo_va_thanhtien()
        if songayo is None or thanhtien is None:
            return
        
        try:
            cur.execute("""INSERT INTO DATPHONG (MaDatPhong, MaKHDatPhong, MaPhong, NgayDat, NgayTra, SoNgayO, SoLuongKhach, MaKHKhac, ThanhTien, GhiChu)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (madp, makh, maphong, ngaydat, ngaytra, songayo, soluong, makhkhac, thanhtien, ghichu))
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm đặt phòng.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm: {str(e)}")

    # Xoá
    def xoa_datphong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để xóa.")
            return
        madp = tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa đặt phòng '{madp}'?")
        if not confirm:
            return
        try:
            cur.execute("DELETE FROM DATPHONG WHERE MaDatPhong = %s", (madp,))
            conn.commit()
            load_data()
            messagebox.showinfo("Đã xóa", f"Đặt phòng {madp} đã được xóa.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa: {str(e)}")

    # Sửa
    def sua_datphong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa.")
            return
        values = tree.item(selected)["values"]
        entry_madp.delete(0, END)
        entry_madp.insert(0, values[0])
        entry_madp.config(state='disabled')  # Khóa Mã đặt phòng
        entry_makh.delete(0, END)
        entry_makh.insert(0, values[1])
        entry_maphong.delete(0, END)
        entry_maphong.insert(0, values[2])
        date_ngaydat.set_date(values[3])
        date_ngaytra.set_date(values[4])
        entry_songayo.delete(0, END)

        madp = entry_madp.get()
        makh = entry_makh.get()
        maphong = entry_maphong.get()
        ngaydat = date_ngaydat.get_date()
        ngaytra = date_ngaytra.get_date()
        soluong = entry_soluong.get()
        makhkhac = entry_makhkhac.get()
        ghichu = entry_ghichu.get()
        
        if not madp or not makh or not maphong:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        
        songayo, thanhtien = tinh_songayo_va_thanhtien()
        if songayo is None or thanhtien is None:
            return
        
        try:
            cur.execute("""UPDATE DATPHONG SET MaKHDatPhong=%s, MaPhong=%s, NgayDat=%s, NgayTra=%s, SoNgayO=%s, SoLuongKhach=%s, MaKHKhac=%s, ThanhTien=%s, GhiChu=%s WHERE MaDatPhong=%s""",
                        (makh, maphong, ngaydat, ngaytra, songayo, soluong, makhkhac, thanhtien, ghichu, madp))
            conn.commit()
            load_data()
            clear_input()
            entry_madp.config(state='normal')  # Mở khóa lại
            messagebox.showinfo("Thành công", "Cập nhật thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {str(e)}")

    # Lưu
    def luu_datphong():
        madp = entry_madp.get()
        makh = entry_makh.get()
        maphong = entry_maphong.get()
        ngaydat = date_ngaydat.get_date()
        ngaytra = date_ngaytra.get_date()
        soluong = entry_soluong.get()
        makhkhac = entry_makhkhac.get()
        ghichu = entry_ghichu.get()
        
        if not madp or not makh or not maphong:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        
        songayo, thanhtien = tinh_songayo_va_thanhtien()
        if songayo is None or thanhtien is None:
            return
        
        try:
            cur.execute("""UPDATE DATPHONG SET MaKHDatPhong=%s, MaPhong=%s, NgayDat=%s, NgayTra=%s, SoNgayO=%s, SoLuongKhach=%s, MaKHKhac=%s, ThanhTien=%s, GhiChu=%s WHERE MaDatPhong=%s""",
                        (makh, maphong, ngaydat, ngaytra, songayo, soluong, makhkhac, thanhtien, ghichu, madp))
            conn.commit()
            load_data()
            clear_input()
            entry_madp.config(state='normal')  # Mở khóa lại
            messagebox.showinfo("Thành công", "Cập nhật thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {str(e)}")

    # Hàm tìm kiếm (lọc theo MaKHDatPhong, điền vào Entry nếu tìm thấy)
    def timkiemtheo_MaKHDatDV():
        search_term = entry_nhapthongtin_timkiem.get().strip()
        if not search_term:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã KH để tìm kiếm.")
            return

        try:
            tree.delete(*tree.get_children())  # Xóa Treeview trước khi query
            cur.execute("SELECT MaDatPhong, MaKHDatPhong, MaPhong, NgayDat, NgayTra, SoNgayO, SoLuongKhach, MaKHKhac, ThanhTien, GhiChu FROM DATPHONG WHERE MaKHDatPhong LIKE %s", (f"%{search_term}%",))
            results = cur.fetchall()
            
            if results:
                # Điền bản ghi đầu tiên vào các Entry (theo thứ tự cột)
                first_row = results[0]
                entry_madp.delete(0, END)
                entry_madp.insert(0, first_row[0])  # MaDatPhong
                entry_makh.delete(0, END)
                entry_makh.insert(0, first_row[1])  # MaKHDatPhong
                entry_maphong.delete(0, END)
                entry_maphong.insert(0, first_row[2])  # MaPhong
                date_ngaydat.set_date(first_row[3])  # NgayDat
                date_ngaytra.set_date(first_row[4])  # NgayTra
                entry_songayo.delete(0, END)
                entry_songayo.insert(0, first_row[5])  # SoNgayO
                entry_soluong.delete(0, END)
                entry_soluong.insert(0, first_row[6])  # SoLuongKhach
                entry_makhkhac.delete(0, END)
                entry_makhkhac.insert(0, first_row[7])  # MaKHKhac
                entry_thanhtien.delete(0, END)
                entry_thanhtien.insert(0, first_row[8])  # ThanhTien
                entry_ghichu.delete(0, END)
                entry_ghichu.insert(0, first_row[9])  # GhiChu
                
                # Hiển thị tất cả kết quả trong Treeview
                for row in results:
                    tree.insert("", END, values=row)
            else:
                messagebox.showinfo("Không tìm thấy", "Không tìm thấy đặt phòng cho mã KH này.")
                load_data()  # Load lại toàn bộ nếu không tìm thấy
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")

    Button(frame_TimKiem, text="Tìm kiếm", width=8, bg="#00AEEF", fg="white", command=timkiemtheo_MaKHDatDV).grid(row=2, column=0, columnspan=3, padx=5)

    # ===== Nút =====
    # ===== Frame nút =====
    frame_btn = Frame(frmDatPhong, bg="#E6F2FA")
    frame_btn.pack(anchor="center", pady=5)

    btn_Them = Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_datphong)
    btn_Them.pack(side=LEFT, padx=5)
    btn_Xoa = Button(frame_btn, text="Xoá", width=8, bg="#00AEEF", fg="white", command=xoa_datphong)
    btn_Xoa.pack(side=LEFT, padx=5)
    btn_Sua = Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_datphong)
    btn_Sua.pack(side=LEFT, padx=5)
    btn_Luu = Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_datphong)
    btn_Luu.pack(side=LEFT, padx=5)
    btn_Huy = Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input)
    btn_Huy.pack(side=LEFT, padx=5)
    btn_Thoat = Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmDatPhong.quit)
    btn_Thoat.pack(side=LEFT, padx=5)
    btn_Refresh = Button(frame_btn, text="Refresh", width=8, bg="#00AEEF", fg="white", command=load_data)
    btn_Refresh.pack(side=LEFT, padx=5)

    # ===== Phân quyền =====
    if vaitro.lower() == 'user':  # Nếu là User, vô hiệu hoá nút thao tác (Trừ nút thoát)
        btn_Them.config(state=DISABLED, bg="gray")
        btn_Xoa.config(state=DISABLED, bg="gray")
        btn_Sua.config(state=DISABLED, bg="gray")
        btn_Luu.config(state=DISABLED, bg="gray")
        btn_Huy.config(state=DISABLED, bg="gray")
        btn_Refresh.config(state=DISABLED, bg="gray")

    frmDatPhong.update_idletasks()
    load_data()
    load_phong_to_combobox()
    frmDatPhong.mainloop()