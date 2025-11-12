from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur  
from Menu import create_menu

def open_form_DatDichVu(vaitro):
    # ====== Hàm canh giữa cửa sổ ======
    def center_window(win, w=900, h=700):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    # ====== Cửa sổ chính ======
    frmDatDV = Tk()
    frmDatDV.title("Đặt Dịch vụ khách sạn")
    frmDatDV.minsize(width=900, height=700)
    center_window(frmDatDV)
    frmDatDV.configure(bg="#E6F2FA")
    frmDatDV.resizable(False, False)

    # ===== Hiển thị menu =====
    create_menu(frmDatDV, "DatDichVu", vaitro)

    # ====== Tiêu đề ======
    Label(frmDatDV, text="QUẢN LÝ ĐẶT DỊCH VỤ KHÁCH SẠN", font=("Times New Roman", 18, "bold"), foreground="#2F4156", bg="#E6F2FA").pack(pady=10)

    # ====== Frame nhập thông tin ====== MaDatDV, MaKHDatDV, MaDV, SoLuongDV, ThanhTien
    frame_info = Frame(frmDatDV, bg="#E6F2FA")
    frame_info.pack(anchor="center", pady=10)

    Label(frame_info, text="Mã đặt DV", font=("Times New Roman", 14, "bold"), foreground="#2F4156",bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_maddv = Entry(frame_info, width=15)
    entry_maddv.grid(row=0, column=1, padx=5, pady=5)

    Label(frame_info, text="Mã KH đặt DV", font=("Times New Roman", 14, "bold"), foreground="#2F4156",bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_makhddv = Entry(frame_info, width=15)
    entry_makhddv.grid(row=0, column=3, padx=5, pady=5)

    Label(frame_info, text="Tên dịch vụ", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    cb_tendv = ttk.Combobox(frame_info, width=20, state="readonly")
    cb_tendv.grid(row=1, column=1, padx=5, pady=5)

    Label(frame_info, text="Mã DV", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_madv = Entry(frame_info, width=15)
    entry_madv.grid(row=1, column=3, padx=5, pady=5)

    Label(frame_info, text="Số lượng", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_soluongDV = Entry(frame_info, width=15)
    entry_soluongDV.grid(row=2, column=1, padx=5, pady=5)

    Label(frame_info, text="Thành tiền", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_thanhtien = Entry(frame_info, width=15)
    entry_thanhtien.grid(row=2, column=3, padx=5, pady=5)

    # Cho các column trong frame_info cân đều
    for i in range(4):  # 4 cột
        frame_info.grid_columnconfigure(i, weight=1, uniform="col")


    # ===== Chức năng tìm kiếm ===== 
    frame_TimKiem = Frame(frmDatDV, bg="#E6F2FA")  
    frame_TimKiem.pack(anchor="center", pady=5)

    # Tiêu đề căn giữa toàn dòng
    Label(frame_TimKiem, text="Tìm kiếm theo mã khách hàng", font=("Times New Roman", 16, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=0, column=0, columnspan=3, pady=(0, 15))

    # Nhãn + Entry + Nút
    Label(frame_TimKiem, text="Nhập mã KH", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=0, pady=5, sticky="e")

    entry_nhapthongtin_timkiem = Entry(frame_TimKiem, width=20)
    entry_nhapthongtin_timkiem.grid(row=1, column=1, pady=5)

    # Chia đều độ rộng các cột trong frame_TimKiem để mọi thứ căn giữa
    frame_TimKiem.grid_columnconfigure(0, weight=1, uniform="col")
    frame_TimKiem.grid_columnconfigure(1, weight=1, uniform="col")
    frame_TimKiem.grid_columnconfigure(2, weight=1, uniform="col")

    
    # ====== Bảng danh sách DV ======
    frame_table = Frame(frmDatDV, bg="#E6F2FA", bd=2, relief="groove")
    frame_table.pack(pady=5, expand=True)

    columns = ("Mã đặt DV", "Mã KH đặt DV", "Mã DV", "Số Lượng DV", "Thành tiền")
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

    tree.pack(padx=10, pady=5, fill="both")

    # ====== Hàm xử lý ======
    # Load dịch vụ cho combobox
    def load_dichvu_to_combobox():
        try:
            cur.execute("SELECT MaDV, TenDV FROM DICHVU")
            dichvu_data = cur.fetchall()
            ten_dichvu_list = [row[1] for row in dichvu_data]
            cb_tendv["values"] = ten_dichvu_list
            # Lưu dict để dễ tra ngược tên -> mã DV
            cb_tendv.dichvu_dict = {row[1]: row[0] for row in dichvu_data}
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi load dịch vụ: {str(e)}")
    
    # Event cho tên dịch vụ
    def on_select_dichvu(event):
        ten_dv = cb_tendv.get()
        if ten_dv in cb_tendv.dichvu_dict:
            entry_madv.delete(0, END)
            entry_madv.insert(0, cb_tendv.dichvu_dict[ten_dv])

    cb_tendv.bind("<<ComboboxSelected>>", on_select_dichvu)


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
    
    # Hàm tính thành tiền tự động
    def tinh_thanhtien():
        try:
            madv = entry_madv.get()
            soluong = int(entry_soluongDV.get())
            if soluong <= 0:
                messagebox.showwarning("Lỗi", "Số lượng phải là số dương.")
                return None
            cur.execute("SELECT GiaDV FROM DICHVU WHERE MaDV = %s", (madv,))
            result = cur.fetchone()
            if not result:
                messagebox.showwarning("Lỗi", f"Không tìm thấy dịch vụ {madv}.")
                return None
            gia = float(result[0])
            return gia * soluong
        except ValueError:
            messagebox.showwarning("Lỗi", "Số lượng phải là số hợp lệ.")
            return None
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tính toán: {str(e)}")
            return None
    
    # Them
    def them_datdichvu():
        maddv = entry_maddv.get()
        makhddv = entry_makhddv.get()
        madv = entry_madv.get()
        soluongDV = entry_soluongDV.get()
        
        if not maddv or not makhddv or not madv or not soluongDV:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ Mã đặt DV, Mã KH, Mã DV, Số lượng.")
            return
        
        thanhtien = tinh_thanhtien()
        if thanhtien is None:
            return
        
        try:
            cur.execute("""INSERT INTO DATDICHVU (MaDatDV, MaKHDatDV, MaDV, SoLuongDV, ThanhTien)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (maddv, makhddv, madv, soluongDV, thanhtien))
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm đặt dịch vụ.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm: {str(e)}")

    # Xoá
    def xoa_datdichvu():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để xóa.")
            return
        maddv = tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa đặt dịch vụ '{maddv}'?")
        if not confirm:
            return
        try:
            cur.execute("DELETE FROM DATDICHVU WHERE MaDatDV = %s", (maddv,))
            conn.commit()
            load_data()
            messagebox.showinfo("Đã xóa", f"Đặt dịch vụ {maddv} đã được xóa.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa: {str(e)}")

    def sua_datdichvu():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa.")
            return
        values = tree.item(selected)["values"]
        entry_maddv.delete(0, END)
        entry_maddv.insert(0, values[0])
        entry_maddv.config(state='disabled')  # Khóa Mã đặt DV
        entry_makhddv.delete(0, END)
        entry_makhddv.insert(0, values[1])
        entry_madv.delete(0, END)
        entry_madv.insert(0, values[2])
        entry_soluongDV.delete(0, END)
        entry_soluongDV.insert(0, values[3])
        entry_thanhtien.delete(0, END)
        entry_thanhtien.insert(0, values[4])
        # Tính lại thành tiền
        thanhtien = tinh_thanhtien()
        if thanhtien is not None:
            entry_thanhtien.delete(0, END)
            entry_thanhtien.insert(0, thanhtien)
    
    def luu_datdichvu():
        maddv = entry_maddv.get()
        makhddv = entry_makhddv.get()
        madv = entry_madv.get()
        soluongDV = entry_soluongDV.get()
        
        if not maddv or not makhddv or not madv or not soluongDV:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        
        thanhtien = tinh_thanhtien()
        if thanhtien is None:
            return
        
        try:
            cur.execute("""UPDATE DATDICHVU SET MaKHDatDV=%s, MaDV=%s, SoLuongDV=%s, ThanhTien=%s WHERE MaDatDV=%s""",
                        (makhddv, madv, soluongDV, thanhtien, maddv))
            conn.commit()
            load_data()
            clear_input()
            entry_maddv.config(state='normal')  # Mở khóa lại
            messagebox.showinfo("Thành công", "Cập nhật thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {str(e)}")

    # Hàm tìm kiếm (lọc theo MaKHDatDV)
    def timkiemtheo_MaKHDatDV():
        search_term = entry_nhapthongtin_timkiem.get().strip()
        if not search_term:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã KH để tìm kiếm.")
            return
        try:
            tree.delete(*tree.get_children()) 
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


    Button(frame_TimKiem, text="Tìm kiếm", width=8, bg="#00AEEF", fg="white", command=timkiemtheo_MaKHDatDV).grid(row=2, column=0, columnspan=3, padx=5)
    # ====== Frame nút ======
    frame_btn = Frame(frmDatDV, bg="#E6F2FA")
    frame_btn.pack(anchor="center", pady=5)

    btn_Them = Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_datdichvu)
    btn_Them.pack(side=LEFT, padx=5)
    btn_Xoa = Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_datdichvu)
    btn_Xoa.pack(side=LEFT, padx=5)
    btn_Sua = Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_datdichvu)
    btn_Sua.pack(side=LEFT, padx=5)
    btn_Luu = Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_datdichvu)
    btn_Luu.pack(side=LEFT, padx=5)
    btn_Huy = Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input)
    btn_Huy.pack(side=LEFT, padx=5)
    btn_Thoat = Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmDatDV.quit)
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
    # ====== Khởi động ======
    load_data()
    load_dichvu_to_combobox()
    frmDatDV.mainloop()
