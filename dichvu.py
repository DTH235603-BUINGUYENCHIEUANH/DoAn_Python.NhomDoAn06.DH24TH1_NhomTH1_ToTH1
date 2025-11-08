from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur  

def open_form_dichvu():
    # ====== Hàm canh giữa cửa sổ ======
    def center_window(win, w=700, h=500):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    # ===== Cửa sổ chính =====
    dichvu = Tk()
    dichvu.title("Dịch vụ - Quản lý khách sạn")
    center_window(dichvu)
    dichvu.configure(bg="#E6F2FA")

    # ==== Title ====
    frame_Title = Frame(dichvu, bg="#E6F2FA")
    Label(frame_Title, text="HỆ THỐNG DỊCH VỤ KHÁCH SẠN TOM AND JERRY", 
          font=("Time news roman",20, "bold"), fg="#2F4156", bg="#E6F2FA").pack()
    frame_Title.pack(pady=10, padx=10, fill="x")

    # ==== Frame nhập thông tin ==== 
    frame_Info = Frame(dichvu, bg="#E6F2FA")
    Label(frame_Info, text="Mã dịch vụ: ", font=("Time news roman",14,"bold"), fg="#2F4156", bg="#E6F2FA").grid(row=0, column=0)
    entry_Madv = Entry(frame_Info, width=10)
    entry_Madv.grid(row=0, column=1)

    Label(frame_Info, text="Tên dịch vụ: ", font=("Time news roman",14,"bold"), fg="#2F4156", bg="#E6F2FA").grid(row=0, column=2)
    entry_Tendv = Entry(frame_Info, width=20)
    entry_Tendv.grid(row=0, column=3)

    Label(frame_Info, text="Giá dịch vụ: ", font=("Time news roman",14,"bold"), fg="#2F4156", bg="#E6F2FA").grid(row=0, column=4)
    entry_GiaDV = Entry(frame_Info, width=10)
    entry_GiaDV.grid(row=0, column=5)
    frame_Info.pack(pady=5, padx=10, fill="x")

    # ====== Bảng danh sách dịch vụ ======
    frame_Table = Frame(dichvu, bg="#E6F2FA")
    Label(frame_Table, text="Danh sách dịch vụ", font=("Time new roman",14,"bold"), fg="#2F4156", bg="#E6F2FA").pack(pady=5, anchor="w", padx=10)
    frame_Table.pack()
    
    columns = ("MãDV", "TênDV", "GiaDV")
    tree = ttk.Treeview(frame_Table, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
    tree.column("MãDV", width=100, anchor="center")
    tree.column("TênDV", width=200)
    tree.column("GiaDV", width=100)
    tree.pack(padx=10, pady=5, fill="both")

    # ===== Hàm xử lý =====
    def clear_input():
        entry_Madv.delete(0, END)
        entry_Tendv.delete(0, END)
        entry_GiaDV.delete(0, END)

    def load_data():
        if conn is None or cur is None:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
            return
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM DICHVU")
        for row in cur.fetchall():
            tree.insert("", END, values=row)

    def them_dichvu():
        madv = entry_Madv.get().strip()
        tendv = entry_Tendv.get().strip()
        giadv = entry_GiaDV.get().strip()

        if not madv or not tendv or not giadv:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            giadv = int(giadv)
            # Kiểm tra xem MaDV đã tồn tại chưa
            cur.execute("SELECT COUNT(*) FROM DICHVU WHERE MaDV = %s", (madv,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Trùng lặp", f"Mã dịch vụ '{madv}' đã tồn tại. Vui lòng chọn mã khác.")
                return
            cur.execute("INSERT INTO DICHVU (MaDV, TenDV, GiaDV) VALUES (%s,%s,%s)", (madv, tendv, giadv))
            conn.commit()
            load_data() 
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm dịch vụ mới.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm: {e}")

    def xoa_dichvu():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để xóa.")
            return
        madv = tree.item(selected)["values"][0]
        #Xác nhận trước khi xoá
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa dịch vụ '{madv}'?")
        if not confirm:
            return
        try:
            cur.execute("DELETE FROM DICHVU WHERE MaDV=%s", (madv,))
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Đã xóa", f"Dịch vụ {madv} đã được xóa.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa: {e}")

    def sua_dichvu():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa.")
            return
        values = tree.item(selected)["values"]
        entry_Madv.delete(0, END); entry_Madv.insert(0, values[0])
        entry_Madv.config(state='disabled')  # Thêm dòng này để khóa MaDV
        entry_Tendv.delete(0, END); entry_Tendv.insert(0, values[1])
        entry_GiaDV.delete(0, END); entry_GiaDV.insert(0, values[2])

    def luu_dichvu():
        madv = entry_Madv.get().strip()
        tendv = entry_Tendv.get().strip()
        giadv = entry_GiaDV.get().strip()

        if not madv or not tendv or not giadv:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            giadv = int(giadv)
            cur.execute("UPDATE DICHVU SET TenDV=%s, GiaDV=%s WHERE MaDV=%s", (tendv, giadv, madv))
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")
        entry_Madv.config(state='normal')  # Mở khóa sau khi lưu

    # ===== Frame Button =====
    frame_Btn = Frame(dichvu, bg="#E6F2FA")
    Button(frame_Btn, text="Thêm", width=8, command=them_dichvu, cursor="hand2").grid(row=0, column=0, padx=5)
    Button(frame_Btn, text="Xoá", width=8, command=xoa_dichvu, cursor="hand2").grid(row=0, column=1, padx=5)
    Button(frame_Btn, text="Sửa", width=8, command=sua_dichvu, cursor="hand2").grid(row=0, column=2, padx=5)
    Button(frame_Btn, text="Lưu", width=8, command=luu_dichvu, cursor="hand2").grid(row=0, column=3, padx=5)
    Button(frame_Btn, text="Thoát", width=8, command=dichvu.destroy, cursor="hand2").grid(row=0, column=4, padx=5)
    frame_Btn.pack(pady=5)

    load_data()
    dichvu.mainloop()
