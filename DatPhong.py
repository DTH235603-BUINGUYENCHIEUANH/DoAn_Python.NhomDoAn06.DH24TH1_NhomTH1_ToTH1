from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from QLKS import conn, cur

def open_form_datphong():
    frmDatPhong = Tk()
    frmDatPhong.title("Quản lý đặt phòng")
    frmDatPhong.geometry("1000x600")
    frmDatPhong.configure(bg="#E6F2FA")
    frmDatPhong.resizable(False, False)

    Label(frmDatPhong, text="QUẢN LÝ ĐẶT PHÒNG", font=("Times New Roman", 18, "bold"), bg="#E6F2FA").pack(pady=10)

    # ===== Frame nhập thông tin =====
    frame_info = Frame(frmDatPhong, bg="#E6F2FA")
    frame_info.pack(anchor="center", pady=10)

    Label(frame_info, text="Mã đặt phòng", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_madp = Entry(frame_info, width=15)
    entry_madp.grid(row=0, column=1, padx=5, pady=5)

    Label(frame_info, text="Mã khách hàng", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_makh = Entry(frame_info, width=15)
    entry_makh.grid(row=0, column=3, padx=5, pady=5)

    Label(frame_info, text="Mã phòng", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_maphong = Entry(frame_info, width=15)
    entry_maphong.grid(row=1, column=1, padx=5, pady=5)

    Label(frame_info, text="Ngày đặt", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    date_ngaydat = DateEntry(frame_info, date_pattern="yyyy-mm-dd", width=12)
    date_ngaydat.grid(row=1, column=3, padx=5, pady=5)

    Label(frame_info, text="Ngày trả", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    date_ngaytra = DateEntry(frame_info, date_pattern="yyyy-mm-dd", width=12)
    date_ngaytra.grid(row=2, column=1, padx=5, pady=5)

    Label(frame_info, text="Số ngày ở", bg="#E6F2FA").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_songayo = Entry(frame_info, width=12)
    entry_songayo.grid(row=2, column=3, padx=5, pady=5)

    Label(frame_info, text="Số lượng khách", bg="#E6F2FA").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_soluong = Entry(frame_info, width=12)
    entry_soluong.grid(row=3, column=1, padx=5, pady=5)

    Label(frame_info, text="Mã khách hàng khác", bg="#E6F2FA").grid(row=3, column=2, padx=5, pady=5, sticky="w")
    entry_makhkhac = Entry(frame_info, width=15)
    entry_makhkhac.grid(row=3, column=3, padx=5, pady=5)

    Label(frame_info, text="Thành tiền", bg="#E6F2FA").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_thanhtien = Entry(frame_info, width=15)
    entry_thanhtien.grid(row=4, column=1, padx=5, pady=5)

    Label(frame_info, text="Ghi chú", bg="#E6F2FA").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    entry_ghichu = Entry(frame_info, width=40)
    entry_ghichu.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="w")

    # ===== Frame nút =====
    frame_btn = Frame(frmDatPhong, bg="#E6F2FA")
    frame_btn.pack(pady=10)
    frame_btn.grid_columnconfigure((0,1,2,3,4,5), weight=1)

    # ===== Chức năng tìm kiếm ===== (Pack trước Treeview để tránh bị che)
    frame_TimKiem = Frame(frmDatPhong, bg="#E6F2FA")  
    frame_TimKiem.pack(anchor="center", pady=20)

    # Tiêu đề căn giữa toàn dòng
    Label(frame_TimKiem, text="Tìm kiếm theo mã khách hàng", font=("Times New Roman", 20, "bold"), bg="#E6F2FA").grid(row=0, column=0, columnspan=3, pady=(0, 15))

    # Nhãn + Entry + Nút
    Label(frame_TimKiem, text="Nhập mã KH", font=("Times New Roman", 11, "bold"), bg="#E6F2FA").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_nhapthongtin_timkiem = Entry(frame_TimKiem, width=20)
    entry_nhapthongtin_timkiem.grid(row=1, column=1, padx=10, pady=5)

    # Chia đều độ rộng các cột trong frame_TimKiem để mọi thứ căn giữa
    frame_TimKiem.grid_columnconfigure(0, weight=1, uniform="col")
    frame_TimKiem.grid_columnconfigure(1, weight=1, uniform="col")
    frame_TimKiem.grid_columnconfigure(2, weight=1, uniform="col")

    # ===== Treeview ===== (Pack sau frame_TimKiem)
    columns = ("MaDatPhong","MaKHDatPhong","MaPhong","NgayDat","NgayTra","SoNgayO","SoLuongKhach","MaKHKhac","ThanhTien","GhiChu")
    tree = ttk.Treeview(frmDatPhong, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(padx=10, pady=10, fill="both")

    # ===== Hàm xử lý =====
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

    # Hàm tìm kiếm (lọc theo MaKHDatPhong, điền vào Entry nếu tìm thấy)
    def timkiemtheo_MaKHDatDV():
        search_term = entry_nhapthongtin_timkiem.get().strip()
        if not search_term:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã KH để tìm kiếm.")
            return
        
        tree.delete(*tree.get_children())  # Xóa Treeview trước khi query
        
        try:
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
    Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=0, padx=5)
    Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmDatPhong.quit).grid(row=0, column=1, padx=5)
    Button(frame_btn, text="Refresh", width=8, bg="#00AEEF", fg="white", command=load_data).grid(row=0, column=2, padx=5)

    load_data()
    frmDatPhong.mainloop()