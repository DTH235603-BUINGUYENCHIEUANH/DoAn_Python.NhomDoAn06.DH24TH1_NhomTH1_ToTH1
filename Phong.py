from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur  


def open_form_phong():
        # ====== Hàm canh giữa cửa sổ ======
        def center_window(win, w=700, h=500):
            ws = win.winfo_screenwidth()
            hs = win.winfo_screenheight()
            x = (ws // 2) - (w // 2)
            y = (hs // 2) - (h // 2)
            win.geometry(f'{w}x{h}+{x}+{y}')

        # ====== Cửa sổ chính ======
        frmPhong = Tk()
        frmPhong.title("Phòng khách sạn")
        center_window(frmPhong, 700, 500)
        frmPhong.configure(bg="#E6F2FA")
        frmPhong.resizable(False, False)

        # ====== Tiêu đề ======
        Label(frmPhong, text="QUẢN LÝ PHÒNG KHÁCH SẠN", font=("Times New Roman", 18, "bold"), foreground="#2F4156", bg="#E6F2FA").pack(pady=10)

        # ====== Frame nhập thông tin ====== 
        frame_info = Frame(frmPhong, bg="#E6F2FA")
        frame_info.pack(pady=5, padx=10, fill="x")

        Label(frame_info, text="Mã phòng", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_maphong = Entry(frame_info, width=15)
        entry_maphong.grid(row=0, column=1, padx=5, pady=5)

        Label(frame_info, text="Tên phòng",font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        entry_tenphong = Entry(frame_info, width=15)
        entry_tenphong.grid(row=0, column=3, padx=5, pady=5)

        Label(frame_info, text="Loại phòng",font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_loaiphong = Entry(frame_info, width=15)
        entry_loaiphong.grid(row=1, column=1, padx=5, pady=5)

        Label(frame_info, text="Giá phòng", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        entry_giaphong = Entry(frame_info, width=15)
        entry_giaphong.grid(row=1, column=3, padx=5, pady=5)

        Label(frame_info, text="Trạng thái", font=("Times New Roman", 14, "bold"), foreground="#2F4156", bg="#E6F2FA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_trangthai = Entry(frame_info, width=15)
        entry_trangthai.grid(row=2, column=1, padx=5, pady=5)

        # ====== Bảng danh sách phòng ======
        Label(frmPhong, text="Danh ságch phòng", font=("Times New Roman", 10, "bold"), foreground="#2F4156", bg="#E6F2FA").pack(pady=5, anchor="w", padx=10)

        columns = ("Mã phòng", "Tên phòng", "Loại phòng", "Giá phòng", "Trạng thái")
        tree = ttk.Treeview(frmPhong, columns=columns, show="headings", height=10)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        tree.pack(padx=10, pady=5, fill="both")


        # ===== Hàm xử lý =====
        def clear_input():
            entry_maphong.delete(0, END)
            entry_tenphong.delete(0, END)
            entry_loaiphong.delete(0, END)
            entry_giaphong.delete(0, END)
            entry_trangthai.delete(0, END)

        def load_data():
            if conn is None or cur is None:
                messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
                return
            tree.delete(*tree.get_children())
            cur.execute("SELECT * FROM PHONG")
            for row in cur.fetchall():
                tree.insert("", END, values=row)

        def them_phong():
            maphong = entry_maphong.get().strip()
            tenphong = entry_tenphong.get().strip()
            loaiphong = entry_loaiphong.get().strip()
            giaphong = entry_giaphong.get().strip()
            trangthai = entry_trangthai.get().strip()

            if not maphong or not tenphong:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
                return
            try:
                # Kiểm tra xem MaDV đã tồn tại chưa MaPhong, TenPhong, LoaiPhong, Gia, TrangThai
                cur.execute("SELECT COUNT(*) FROM PHONG WHERE MaPhong = %s", (maphong,))
                if cur.fetchone()[0] > 0:
                    messagebox.showwarning("Trùng lặp", f"Mã phòng '{maphong}' đã tồn tại. Vui lòng chọn mã khác.")
                    return
                cur.execute("INSERT INTO PHONG (MaPhong, TenPhong, LoaiPhong, Gia, TrangThai) VALUES (%s, %s, %s, %s, %s)", (maphong, tenphong, loaiphong, giaphong, trangthai))
                conn.commit()
                load_data() 
                clear_input()
                messagebox.showinfo("Thành công", "Đã thêm dịch vụ mới.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm: {e}")

        def xoa_phong():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để xóa.")
                return
            maphong = tree.item(selected)["values"][0]
            #Xác nhận trước khi xoá
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phòng '{maphong}'?")
            if not confirm:
                return
            try:
                cur.execute("DELETE FROM PHONG WHERE MaPhong=%s", (maphong,))
                conn.commit()
                load_data()
                clear_input()
                messagebox.showinfo("Đã xóa", f"Phòng {maphong} đã được xóa.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa: {e}")

        def sua_phong():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa.")
                return
            values = tree.item(selected)["values"]
            entry_maphong.delete(0, END); entry_maphong.insert(0, values[0])
            entry_maphong.config(state='disabled')  # Thêm dòng này để khóa MaDV
            entry_tenphong.delete(0, END); entry_tenphong.insert(0, values[1])
            entry_loaiphong.delete(0, END); entry_loaiphong.insert(0, values[2])
            entry_giaphong.delete(0, END); entry_giaphong.insert(0, values[3])
            entry_trangthai.delete(0, END); entry_trangthai.insert(0, values[4])

        def luu_phong():
            maphong = entry_maphong.get().strip()
            tenphong = entry_tenphong.get().strip()
            loaiphong = entry_loaiphong.get().strip()
            giaphong = entry_giaphong.get().strip()
            trangthai = entry_trangthai.get().strip()

            if not maphong or not tenphong:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
                return
            try:
                giaphong = int(giaphong)
                cur.execute("UPDATE PHONG SET TenPhong=%s, LoaiPhong=%s, GiaPhong=%s, TrangThai=%s WHERE MaDV=%s", (maphong, tenphong, loaiphong, giaphong, trangthai))
                conn.commit()
                load_data()
                clear_input()
                messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")
            entry_maphong.config(state='normal')  # Mở khóa sau khi lưu

        # ====== Frame nút ======
        frame_btn = Frame(frmPhong, bg="#E6F2FA")
        frame_btn.pack(pady=5)

        Button(frame_btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_phong).grid(row=0, column=0, padx=5)
        Button(frame_btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_phong).grid(row=0, column=1, padx=5)
        Button(frame_btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_phong).grid(row=0, column=2, padx=5)
        Button(frame_btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input).grid(row=0, column=3, padx=5)
        Button(frame_btn, text="Xóa", width=8, bg="#00AEEF", fg="white", command=xoa_phong).grid(row=0, column=4, padx=5)
        Button(frame_btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=frmPhong.quit).grid(row=0, column=5, padx=5)

        # ====== Khởi động ======

        load_data()
        frmPhong.mainloop()