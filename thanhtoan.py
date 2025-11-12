from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur
from Menu import create_menu

def open_form_ThanhToan(vaitro):
    # ====== Hàm canh giữa cửa sổ ======
    def center_window(win, w=800, h=500):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')
        
    # ===== Cửa sổ chính =====
    hoadon = Tk()
    hoadon.title("Hoá đơn - Quản lý khách sạn")
    hoadon.minsize(width=800, height=500)
    center_window(hoadon)
    hoadon.configure(bg="#E6F2FA")

    # ===== Hiển thị menu =====
    create_menu(hoadon, "ThanhToan", vaitro)
    # ==== Title ====
    frame_Title = Frame(hoadon)
    Label(frame_Title, text="HỆ THỐNG HOÁ ĐƠN KHÁCH SẠN TOM AND JERRY", font=("Time news roman",20, "bold"), foreground="#2F4156", background="#E6F2FA")
    frame_Title.pack(pady=10, padx=10, fill="x", anchor=CENTER)
    frame_Title.configure(bg="#E6F2FA")

    # ==== Frame nhập thông tin ==== 
    frame_Info = Frame(hoadon)
    frame_Info.pack(pady=20, padx=10)
    frame_Info.configure(bg="#E6F2FA")

    # ====== Thông tin hoá đơn ====== 
    lbl_mahd = Label(frame_Info, text="Mã hoá đơn", font=("Times New Roman", 14, "bold"), foreground="#2F4156", background="#E6F2FA")
    lbl_mahd.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_mahd = Entry(frame_Info, width=15)
    entry_mahd.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    lbl_manvtt = Label(frame_Info, text="Mã nhân viên thanh toán", font=("Times New Roman", 14, "bold"), foreground="#2F4156", background="#E6F2FA")
    lbl_manvtt.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_manvtt = Entry(frame_Info, width=15)
    entry_manvtt.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    lbl_makh = Label(frame_Info, text="Mã khách hàng", font=("Times New Roman", 14, "bold"), foreground="#2F4156", background="#E6F2FA")
    lbl_makh.grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_makh = Entry(frame_Info, width=15)
    entry_makh.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    lbl_phuongthuctt = Label(frame_Info, text="Phương thức thanh toán", font=("Times New Roman", 14, "bold"),foreground="#2F4156", background="#E6F2FA")
    lbl_phuongthuctt.grid(row=1, column=2, padx=5, pady=5, sticky="e")
    entry_phuongthuctt = Entry(frame_Info, width=15)
    entry_phuongthuctt.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    lbl_tongtien = Label(frame_Info, text="Tổng tiền", font=("Times New Roman", 14, "bold"),foreground="#2F4156", background="#E6F2FA")
    lbl_tongtien.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_tongtien = Entry(frame_Info, width=15)
    entry_tongtien.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # ====== Bảng danh sách hoá đơn ====== MaHoaDon, MaNVThanhToan, MaKH, MaPhong, MaDVDaDat, TienPhong, TienDV, TongTien
    # Tạo frame chứa bảng và thanh cuộn
    frame_table = Frame(hoadon, bg="#E6F2FA", bd=2, relief="groove")
    frame_table.pack(pady=5, expand=True)
    frame_table.configure(background="#E6F2FA")

    columns = ("Mã hoá đơn", "Mã NV Thanh toán", "Mã KH", "Phương thức thanh toán", "Tổng tiền")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)

    # ====== Thanh cuộn ======
    scroll_y = Scrollbar(frame_table, orient="vertical", command=tree.yview, bg="#E6F2FA")
    tree.configure(yscrollcommand=scroll_y.set)

    # ====== Đặt vị trí ======
    scroll_y.pack(side="right", fill="y")
    tree.pack(side="left", expand=True)

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column("Mã hoá đơn", width=100, anchor="center")
        tree.column("Mã NV Thanh toán", width=100)
        tree.column("Mã KH", width=100)
        tree.column("Phương thức thanh toán", width=150)
        tree.column("Tổng tiền", width=100)
        tree.pack(pady=5)

     # ===== Hàm xử lý =====
    def clear_input():
        entry_mahd.delete(0, END)
        entry_manvtt.delete(0, END)
        entry_makh.delete(0, END)
        entry_phuongthuctt.delete(0, END)
        entry_tongtien.delete(0, END)

    def load_data():
        if conn is None or cur is None:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
            return
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM HOADON")
        for row in cur.fetchall():  
            tree.insert("", END, values=row)  


    def them_thanhtoan():
        mahd = entry_mahd.get()
        manvtt = entry_manvtt.get()
        makh = entry_makh.get()
        phuongthuctt = entry_phuongthuctt.get()
        tongtien = entry_tongtien.get()
        tong_tien = tinh_tong_tien(makh)
        entry_tongtien.delete(0, END)
        entry_tongtien.insert(0, str(tong_tien))

        # Kiểm tra kiểu dữ liệu
        try:
            tongtien = float(tong_tien)  # Chuyển sang float để đảm bảo
        except ValueError:
            messagebox.showwarning("Lỗi", "Tổng tiền phải là số hợp lệ.")
            return
        
        # Kiểm tra phương thức thanh toán 
        if phuongthuctt not in ['Chuyen khoan', 'Tien mat']:
            messagebox.showwarning("Lỗi", "Phương thức thanh toán phải là 'Chuyen khoan' hoặc 'Tien mat'.")
            return
        
        if not mahd or not makh or not manvtt:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin bắt buộc.")
            return
        try:
            cur.execute("""INSERT INTO HOADON (MaHoaDon, MaNVThanhToan, MaKH, PhuongThucTT, TongTien)
                           VALUES (%s,%s,%s,%s,%s)""",
                        (mahd, manvtt, makh, phuongthuctt, tongtien))
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm hoá đơn mới.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm: {e}")

    def xoa_thanhtoan():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để xóa.")
            return
        mahd = tree.item(selected)["values"][0]
        #Xác nhận trước khi xoá
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa hoá đơn '{mahd}'?")
        if not confirm:
            return
        
        try:
            cur.execute("DELETE FROM HOADON WHERE MaHoaDon=%s", (mahd,))
            conn.commit()
            load_data()
            messagebox.showinfo("Đã xóa", f"Hoá đơn {mahd} đã được xóa.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa: {e}")

    def sua_thanhtoan():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa.")
            return
        values = tree.item(selected)["values"]
        entry_mahd.delete(0, END); entry_mahd.insert(0, values[0])  # Mã hoá đơn
        entry_mahd.config(state='disabled')  # Khóa ô Mã hoá đơn
        entry_manvtt.delete(0, END); entry_manvtt.insert(0, values[1])  # Mã NV Thanh toán
        entry_makh.delete(0, END); entry_makh.insert(0, values[2])  # Mã KH
        entry_phuongthuctt.delete(0, END); entry_phuongthuctt.insert(0, values[3])  # Phương thức TT
        #entry_tongtien.delete(0, END); entry_tongtien.insert(0, values[4])  # Tổng tiền
        tong_tien_moi = tinh_tong_tien(values[2])  # Tính lại dựa trên MaKH cũ
        entry_tongtien.delete(0, END); entry_tongtien.insert(0, str(tong_tien_moi))  # Cập nhật tổng tiền mới
    
    def luu_thanhtoan():
        mahd = entry_mahd.get()
        manvtt = entry_manvtt.get()
        makh = entry_makh.get()
        phuongthuctt = entry_phuongthuctt.get()
        tongtien = entry_tongtien.get()

         # Thêm kiểm tra kiểu dữ liệu
        try:
            tongtien = float(tongtien)
        except ValueError:
            messagebox.showwarning("Lỗi", "Tổng tiền phải là số hợp lệ.")
            return
        # Thêm kiểm tra phương thức thanh toán
        if phuongthuctt not in ['Chuyen khoan', 'Tien mat']:
            messagebox.showwarning("Lỗi", "Phương thức thanh toán phải là 'Chuyen khoan' hoặc 'Tien mat'.")
            return

        if not mahd or not makh or not manvtt:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin bắt buộc.")
            return
        try:
            # Chỉ update các field không phải primary key
            cur.execute("""UPDATE HOADON SET MaNVThanhToan=%s, MaKH=%s, PhuongThucTT=%s, TongTien=%s WHERE MaHoaDon=%s""",
                        (manvtt, makh, phuongthuctt, tongtien, mahd))
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
            entry_mahd.config(state='normal')  # Mở khóa lại sau khi lưu
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")
    
    # ===== Hàm tính tổng tiền 
    def tinh_tong_tien(makh):
        try:
            # Tổng tiền phòng từ DATPHONG
            cur.execute("SELECT IFNULL(SUM(ThanhTien), 0) FROM DATPHONG WHERE MaKHDatPhong = %s", (makh,))
            tien_phong = float(cur.fetchone()[0])
            # Tổng tiền dịch vụ từ DATDICHVU
            cur.execute("SELECT IFNULL(SUM(ThanhTien), 0) FROM DATDICHVU WHERE MaKHDatDV = %s", (makh,))
            tien_dv = float(cur.fetchone()[0])
            return tien_phong + tien_dv
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tính tiền: {e}")
            return 0

    # ===== Frame Button =====
    frame_Btn = Frame(hoadon)
    btn_Them = Button(frame_Btn, text="Thêm", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#00AEEF", command=them_thanhtoan)
    btn_Them.grid(row=0, column=0, padx=5)
    btn_Xoa = Button(frame_Btn, text="Xoá", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#00AEEF", command=xoa_thanhtoan)
    btn_Xoa.grid(row=0, column=1, padx=5)
    btn_Sua = Button(frame_Btn, text="Sửa", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#00AEEF", command=sua_thanhtoan)
    btn_Sua.grid(row=0, column=2, padx=5)
    btn_Luu = Button(frame_Btn, text="Lưu", width=8,  font=("Time news roman",10), foreground="#2F4156", background="#00AEEF", command=luu_thanhtoan)
    btn_Luu.grid(row=0, column=3, padx=5)
    btn_Huy = Button(frame_Btn, text="Hủy", width=8, background="#00AEEF", foreground="#2F4156", cursor="hand2", command=clear_input)
    btn_Huy.grid(row=0, column=4, padx=5)
    btn_Thoat = Button(frame_Btn, text="Thoát", width=8, font=("Time news roman",10), foreground="#2F4156", background="#00AEEF", command=hoadon.quit)
    btn_Thoat.grid(row=0, column=5, padx=5)
    btn_Refresh = Button(frame_Btn, text="Refresh", width=8, background="#00AEEF", foreground="#2F4156", command=load_data)
    btn_Refresh.grid(row=0, column=6, padx=5)

    frame_Btn.pack(pady=5)

    # ===== Phân quyền =====
    if vaitro.lower() == 'user':  # Nếu là User, vô hiệu hoá nút thao tác (Trừ nút thoát)
        btn_Them.config(state=DISABLED, bg="gray")
        btn_Xoa.config(state=DISABLED, bg="gray")
        btn_Sua.config(state=DISABLED, bg="gray")
        btn_Luu.config(state=DISABLED, bg="gray")
        btn_Huy.config(state=DISABLED, bg="gray")
        btn_Refresh.config(state=DISABLED, bg="gray")

    load_data()
    hoadon.mainloop()