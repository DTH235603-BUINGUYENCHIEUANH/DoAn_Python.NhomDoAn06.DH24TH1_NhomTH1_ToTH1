from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur  

def open_form_datdichvu():
    # ====== Hàm canh giữa cửa sổ ======
    def center_window(win, w=700, h=500):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    # ====== Cửa sổ chính ======
    frmDatDV = Tk()
    frmDatDV.title("Đặt Dịch vụ khách sạn")
    frmDatDV.minsize(width=900, height=500)
    frmDatDV.configure(bg="#E6F2FA")
    frmDatDV.resizable(False, False)

    # ====== Tiêu đề ======
    Label(frmDatDV, text="QUẢN LÝ ĐẶT DỊCH VỤ KHÁCH SẠN", font=("Times New Roman", 18, "bold"), bg="#E6F2FA").pack(pady=10)

    # ====== Frame nhập thông tin ====== MaDatDV, MaKHDatDV, MaDV, SoLuongDV, ThanhTien
    frame_info = Frame(frmDatDV, bg="#E6F2FA")
    frame_info.pack(anchor="center", pady=10)

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

    # ===== Chức năng tìm kiếm ===== 
    frame_TimKiem = Frame(frmDatDV, bg="#E6F2FA")  
    frame_TimKiem.pack(anchor="center", pady=20)

    # Tiêu đề căn giữa toàn dòng
    Label(frame_TimKiem, 
        text="Tìm kiếm theo mã khách hàng", 
        font=("Times New Roman", 20, "bold"), 
        bg="#E6F2FA").grid(row=0, column=0, columnspan=3, pady=(0, 15))

    # Nhãn + Entry + Nút
    Label(frame_TimKiem, 
        text="Nhập mã KH", 
        font=("Times New Roman", 11, "bold"), 
        bg="#E6F2FA").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_nhapthongtin_timkiem = Entry(frame_TimKiem, width=20)
    entry_nhapthongtin_timkiem.grid(row=1, column=1, padx=10, pady=5)

    # Chia đều độ rộng các cột trong frame_TimKiem để mọi thứ căn giữa
    frame_TimKiem.grid_columnconfigure(0, weight=1, uniform="col")
    frame_TimKiem.grid_columnconfigure(1, weight=1, uniform="col")
    frame_TimKiem.grid_columnconfigure(2, weight=1, uniform="col")

    
    # ====== Bảng danh sách phòng ======
    Label(frmDatDV, text="Danh sách đặt DV", font=("Times New Roman", 10, "bold"), bg="#E6F2FA").pack(pady=5, anchor="w", padx=10)

    columns = ("Mã đặt DV", "Mã KH đặt DV", "Mã DV", "Số Lượng DV", "Thành tiền")
    tree = ttk.Treeview(frmDatDV, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(padx=10, pady=5, fill="both")

    # ====== Hàm xử lý ======
    # Clear
    def clear_input():
        entry_maddv.delete(0, END)
        entry_makhddv.delete(0, END)
        entry_madv.delete(0, END)
        entry_soluongDV.delete(0, END)
        entry_thanhtien.delete(0, END)
    
    # Load data
    def load_data():
        if conn is None or cur is None:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
            return
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM DATDICHVU")
        for row in cur.fetchall():
            tree.insert("", END, values=row)

        entry_maddv.delete(0, END)
        entry_makhddv.delete(0, END)
        entry_madv.delete(0, END)
        entry_soluongDV.delete(0, END)
        entry_thanhtien.delete(0, END) 
        entry_nhapthongtin_timkiem.delete(0, END)    
    
    # Hàm tìm kiếm (lọc theo MaKHDatDV)
    def timkiemtheo_MaKHDatDV():
        search_term = entry_nhapthongtin_timkiem.get().strip()
        if not search_term:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã KH để tìm kiếm.")
            return
        try:
            cur.execute("SELECT MaDatDV, MaKHDatDV, MaDV, SoLuongDV, ThanhTien FROM DATDICHVU WHERE MaKHDatDV LIKE %s", (f"%{search_term}%",))
            results = cur.fetchall()
                
            if results:
                # Điền bản ghi đầu tiên vào các Entry
                first_row = results[0]
                entry_maddv.delete(0, END)
                entry_maddv.insert(0, first_row[0])  # MaDatDV
                entry_makhddv.delete(0, END)
                entry_makhddv.insert(0, first_row[1])  # MaKHDatDV
                entry_madv.delete(0, END)
                entry_madv.insert(0, first_row[2])  # MaDV
                entry_soluongDV.delete(0, END)
                entry_soluongDV.insert(0, first_row[3])  # SoLuongDV
                entry_thanhtien.delete(0, END)
                entry_thanhtien.insert(0, first_row[4])  # ThanhTien
                    
                # Hiển thị tất cả kết quả trong Treeview
                for row in results:
                    tree.insert("", END, values=row)
            else:
                messagebox.showinfo("Không tìm thấy", "Không tìm thấy đặt dịch vụ cho mã KH này.")
                # Nếu không có, vẫn có thể để Treeview trống hoặc load lại toàn bộ (tùy bạn)
                load_data()  # Tùy chọn: load lại toàn bộ nếu không tìm thấy
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")
    
        tree.delete(*tree.get_children())

    Button(frame_TimKiem, text="Tìm kiếm", width=8, bg="#00AEEF", fg="white", command=timkiemtheo_MaKHDatDV).grid(row=2, column=0, columnspan=3, padx=5)
    # ====== Frame nút ======
    frame_btn = Frame(frmDatDV, bg="#E6F2FA")
    frame_btn.pack(pady=5)

    Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=0, padx=5)
    Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmDatDV.quit).grid(row=0, column=1, padx=5)
    Button(frame_btn, text="Refresh", width=8, bg="#00AEEF", fg="white", command=load_data).grid(row=0, column=2, padx=5)
    # ====== Khởi động ======
    load_data()
    frmDatDV.mainloop()
