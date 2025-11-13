from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import csv
from tkinter import filedialog, messagebox
from datetime import datetime, date
from QLKS import conn, cur  
from ChatBot import open_chatbot, add_chatbot_button 
from Menu import create_menu

def open_form_NhanVien(vaitro):
    # ====== Hàm canh giữa cửa sổ ======
    def center_window(win, w=800, h=600):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    # ====== Cửa sổ chính ======
    frmNhanVien = Tk()
    frmNhanVien.title("Quản lý nhân viên khách sạn Tom & Jerry")
    frmNhanVien.minsize(width=800, height=600)
    center_window(frmNhanVien)
    frmNhanVien.configure(bg="#E6F2FA")
    frmNhanVien.resizable(False, False)

    # ===== Hiển thị menu =====
    create_menu(frmNhanVien, "NhanVien", vaitro)

    # ===== Chatbot =====
    add_chatbot_button(frmNhanVien, x_offset=-10, y_offset=40)
    
    # ====== Tiêu đề ======
    lbl_title = Label(frmNhanVien, text="QUẢN LÝ NHÂN VIÊN KHÁCH SẠN TOM & JERRY", foreground="#2F4156", font=("Times New Roman", 18, "bold"), bg="#E6F2FA")
    lbl_title.pack(pady=5)

    
    # ====== Frame nhập thông tin ======
    frame_info = Frame(frmNhanVien, bg="#E6F2FA")
    frame_info.pack(pady=5, padx=5)

    Label(frame_info, text="Mã nhân viên", font=("Times New Roman", 14), fg="#2F4156", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_manv = Entry(frame_info, width=15)
    entry_manv.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Họ tên NV", font=("Times New Roman", 14), fg="#2F4156", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_hoten = Entry(frame_info, width=25)
    entry_hoten.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Giới tính", font=("Times New Roman", 14), fg="#2F4156", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_gioitinh = Entry(frame_info, width=15)
    entry_gioitinh.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Ngày sinh", font=("Times New Roman", 14), fg="#2F4156", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    date_ngaysinh = DateEntry(frame_info, date_pattern="yyyy-mm-dd", width=12)
    date_ngaysinh.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    Label(frame_info, text="Chức vụ", font=("Times New Roman", 14), fg="#2F4156", bg="#E6F2FA").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    entry_chucvu = Entry(frame_info, width=15)
    entry_chucvu.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    # Thiết lập grid đều nhau
    for i in range(4):  # giả sử có 4 cột
        frame_info.columnconfigure(i, weight=1, uniform="col")  # uniform giúp các cột đều nhau

    # Load
    def load_data():
        if conn is None or cur is None:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
            return
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM NHANVIEN")
        for row in cur.fetchall():
            tree.insert("", END, values=row)
    
    # ====== Bảng danh sách nhân viên ====== 
    # Tạo frame chứa bảng và thanh cuộn
    frame_table = Frame(frmNhanVien, bg="#E6F2FA", bd=2, relief="groove")
    frame_table.pack(pady=5, expand=True)
    frame_table.configure(background="#E6F2FA")

    # ===== Treeview ===== (Pack sau frame_TimKiem)
    columns = ("Mã nhân viên", "Họ tên NV", "Giới tính", "Ngày sinh", "Chức vụ")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=8)

    # ====== Thanh cuộn ======
    scroll_y = Scrollbar(frame_table, orient="vertical", command=tree.yview, bg="#E6F2FA")
    tree.configure(yscrollcommand=scroll_y.set)

    # ====== Đặt vị trí ======
    scroll_y.pack(side="right", fill="y")
    tree.pack(side="left", expand=True)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(padx=5, pady=10, fill="x")

    # ====== Chức năng ======
    # ===== Hàm xử lý =====

    # Clear
    def clear_input():
        entry_manv.delete(0, END)
        entry_hoten.delete(0, END)
        entry_gioitinh.delete(0, END)
        entry_chucvu.delete(0, END)
        date_ngaysinh.set_date("2025-01-01")

    # Thêm
    def them_nhanvien():
        manv = entry_manv.get().strip() 
        hoten = entry_hoten.get().strip()
        gioitinh = entry_gioitinh.get().strip()
        ngaysinh = date_ngaysinh.get_date()
        chucvu = entry_chucvu.get().strip()

        if not manv or not hoten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            # Kiểm tra xem MaNV đã tồn tại chưa 
            cur.execute("SELECT COUNT(*) FROM NHANVIEN WHERE MaNV = %s", (manv,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Trùng lặp", f"Mã nhân viên '{manv}' đã tồn tại. Vui lòng chọn mã khác.")
                return
            
            cur.execute("INSERT INTO NHANVIEN (MaNV, HoTenNV, GioiTinh, NgaySinh, ChucVu) VALUES (%s,%s,%s,%s,%s)", (manv, hoten, gioitinh, ngaysinh, chucvu))
            conn.commit()
            load_data() 
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm nhân viên mới.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm: {e}")

    # Xoá
    def xoa_nhanvien():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để xóa.")
            return
        manv = tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa đặt phòng '{manv}'?")
        if not confirm:
            return
        try:
            cur.execute("DELETE FROM NHANVIEN WHERE MaNV = %s", (manv,))
            conn.commit()
            load_data()
            messagebox.showinfo("Đã xóa", f"Nhân viên {manv} đã được xóa.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa: {str(e)}")

    # Sửa
    def sua_nhanvien():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa.")
            return
        values = tree.item(selected)["values"]
        entry_manv.delete(0, END), entry_manv.insert(0, values[0])
        entry_manv.config(state='disabled')  # Khóa Mã nhân viên
        entry_hoten.delete(0, END), entry_hoten.insert(0, values[1])
        entry_gioitinh.delete(0, END), entry_gioitinh.insert(0, values[2])
        entry_chucvu.delete(0, END), entry_chucvu.insert(0, values[3])
        date_ngaysinh.set_date(values[4])
        
        

        manv = entry_manv.get()
        hoten = entry_hoten.get()
        gioitinh = entry_gioitinh.get()
        ngaysinh = date_ngaysinh.get_date()
        chucvu = entry_chucvu.get()
        
        if not manv or not hoten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        
        try: # NHANVIEN (MaNV, HoTenNV, GioiTinh, NgaySinh, ChucVu)
            cur.execute("""UPDATE NHANVIEN SET MaNV=%s, HoTenNV=%s, GioiTinh=%s, NgaySinh=%s, ChucVu=%s""",
                        (manv, hoten, gioitinh, ngaysinh, chucvu))
            conn.commit()
            load_data()
            clear_input()
            entry_manv.config(state='normal')  # Mở khóa lại
            messagebox.showinfo("Thành công", "Cập nhật thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {str(e)}")

    # Lưu
    def luu_nhanvien():
        manv = entry_manv.get().strip() 
        hoten = entry_hoten.get().strip()
        gioitinh = entry_gioitinh.get().strip()
        ngaysinh = date_ngaysinh.get_date()
        chucvu = entry_chucvu.get().strip()
        
        if not manv or not hoten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        
        try:
            cur.execute("""UPDATE NHANVIEN SET MaNV=%s, HoTenNV=%s, GioiTinh=%s, NgaySinh=%s, ChucVu=%s""",
                        (manv, hoten, gioitinh, ngaysinh, chucvu))
            conn.commit()
            load_data()
            clear_input()
            entry_manv.config(state='normal')  # Mở khóa lại
            messagebox.showinfo("Thành công", "Cập nhật thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {str(e)}")
    
    # ===== In thông tin toàn bộ nhân viên =====
    def xuat_nhanvien():
        # Chọn nơi lưu file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="DanhSachNhanVien.csv",
            initialdir="C:/Users/YourUserName/Documents"
        )
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # ===== Ghi tiêu đề =====
                writer.writerow(["Mã nhân viên", "Họ tên NV", "Giới tính", "Ngày sinh", "Chức vụ"])
                
                # Lấy dữ liệu từ DB
                cur.execute("SELECT MaNV, HoTenNV, GioiTinh, NgaySinh, ChucVu FROM NHANVIEN")
                rows = cur.fetchall()
                
                for row in rows:
                    row_list = list(row)
                    # Format ngày sinh nếu là datetime/date
                    if isinstance(row_list[3], (datetime, date)):
                        row_list[3] = row_list[3].strftime("%Y-%m-%d")  # Hoặc "%d/%m/%Y"
                    writer.writerow(row_list)

            messagebox.showinfo("Thành công", f"Đã xuất toàn bộ nhân viên ra {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xuất nhân viên: {e}")
    
    # ===== Frame nút =====
    frame_btn = Frame(frmNhanVien, bg="#E6F2FA")
    frame_btn.pack(anchor="center", pady=5)

    btn_Them = Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_nhanvien)
    btn_Them.pack(side=LEFT, padx=5)
    btn_Xoa = Button(frame_btn, text="Xoá", width=8, bg="#00AEEF", fg="white", command=xoa_nhanvien)
    btn_Xoa.pack(side=LEFT, padx=5)
    btn_Sua = Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_nhanvien)
    btn_Sua.pack(side=LEFT, padx=5)
    btn_Luu = Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_nhanvien)
    btn_Luu.pack(side=LEFT, padx=5)
    btn_Huy = Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input)
    btn_Huy.pack(side=LEFT, padx=5)
    btn_Thoat = Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmNhanVien.quit)
    btn_Thoat.pack(side=LEFT, padx=5)
    btn_Reset = Button(frame_btn, text="Reset", width=8, bg="#00AEEF", fg="white", command=load_data)
    btn_Reset.pack(side=LEFT, padx=5)
    btn_Xuat = Button(frame_btn, text="Xuất TT Nhân viên", width=15, bg="#00AEEF", fg="white", command=xuat_nhanvien)
    btn_Xuat.pack(side=LEFT, padx=5)


    # ===== Phân quyền =====
    if vaitro.lower() == 'user':  # Nếu là User, vô hiệu hoá nút thao tác (Trừ nút thoát)
        btn_Them.config(state=DISABLED, bg="gray")
        btn_Xoa.config(state=DISABLED, bg="gray")
        btn_Sua.config(state=DISABLED, bg="gray")
        btn_Luu.config(state=DISABLED, bg="gray")
        btn_Huy.config(state=DISABLED, bg="gray")
        btn_Reset.config(state=DISABLED, bg="gray")
        btn_Xuat.config(state=DISABLED, bg="gray")

    load_data()
    frmNhanVien.mainloop()
