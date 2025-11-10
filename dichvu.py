from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from QLKS import conn, cur  

def open_form_dichvu(vaitro):
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
    Label(frame_Info, text="Mã dịch vụ: ", font=("Time news roman",14,"bold"), fg="#2F4156", bg="#E6F2FA").grid(row=0, column=2)
    entry_Madv = Entry(frame_Info, width=10)
    entry_Madv.grid(row=0, column=3)

    Label(frame_Info, text="Tên dịch vụ: ", font=("Time news roman",14,"bold"), fg="#2F4156", bg="#E6F2FA").grid(row=0, column=0)
    entry_Tendv = Entry(frame_Info, width=10)
    entry_Tendv.grid(row=0, column=1)
    '''cb_Tendv = ttk.Combobox(frame_Info, width=20, state="readonly")   # <== thay Entry bằng Combobox
    cb_Tendv.grid(row=0, column=1)'''

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
    # ====== Hàm nạp dữ liệu cho Combobox Tên dịch vụ ======
    '''def load_dichvu_to_combobox():
        cur.execute("SELECT MaDV, TenDV, GiaDV FROM DICHVU")
        dichvu_data = cur.fetchall()
        ten_dichvu_list = [row[1] for row in dichvu_data]
        cb_Tendv["values"] = ten_dichvu_list

        # Lưu lại dict để dễ truy xuất ngược theo tên dịch vụ
        cb_Tendv.dichvu_dict = {row[1]: (row[0], row[2]) for row in dichvu_data}

    # ====== Khi chọn tên dịch vụ trong combobox ======
    def on_select_dichvu(event):
        ten_dv = cb_Tendv.get()
        if ten_dv in cb_Tendv.dichvu_dict:
            madv, giadv = cb_Tendv.dichvu_dict[ten_dv]
            entry_Madv.delete(0, END)
            entry_Madv.insert(0, madv)
            entry_GiaDV.delete(0, END)
            entry_GiaDV.insert(0, giadv)

    cb_Tendv.bind("<<ComboboxSelected>>", on_select_dichvu)'''

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
            #load_dichvu_to_combobox() #Cập nhật dịch vụ mới cho combobox dịch vụ
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
            #load_dichvu_to_combobox()
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
            #load_dichvu_to_combobox() 
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")
        entry_Madv.config(state='normal')  # Mở khóa sau khi lưu

    # ===== Frame Button =====
    frame_Btn = Frame(dichvu, bg="#E6F2FA")
    frame_Btn.pack(pady=5)

    btn_Them = Button(frame_Btn, text="Thêm", width=8, bg="#00AEEF", fg="white", command=them_dichvu, cursor="hand2")
    btn_Them.grid(row=0, column=0, padx=5)
    btn_Xoa = Button(frame_Btn, text="Xoá", width=8, bg="#00AEEF", fg="white", command=xoa_dichvu, cursor="hand2")
    btn_Xoa.grid(row=0, column=1, padx=5)
    btn_Sua = Button(frame_Btn, text="Sửa", width=8, bg="#00AEEF", fg="white", command=sua_dichvu, cursor="hand2")
    btn_Sua.grid(row=0, column=2, padx=5)
    btn_Luu = Button(frame_Btn, text="Lưu", width=8, bg="#00AEEF", fg="white", command=luu_dichvu, cursor="hand2")
    btn_Luu.grid(row=0, column=3, padx=5)
    btn_Thoat = Button(frame_Btn, text="Thoát", width=8, bg="#00AEEF", fg="white", command=dichvu.destroy, cursor="hand2")
    btn_Thoat.grid(row=0, column=4, padx=5)
    btn_Huy = Button(frame_Btn, text="Hủy", width=8, bg="#00AEEF", fg="white", command=clear_input)
    btn_Huy.grid(row=0, column=5, padx=5)
    btn_Refresh = Button(frame_Btn, text="Refresh", width=8, bg="#00AEEF", fg="white", command=load_data)
    btn_Refresh.grid(row=0, column=6, padx=5)
   
    # ===== Phân quyền =====
    if vaitro.lower() == 'user':  # Nếu là User, vô hiệu hoá nút thao tác (Trừ nút thoát)
        btn_Them.config(state=DISABLED, bg="gray")
        btn_Xoa.config(state=DISABLED, bg="gray")
        btn_Sua.config(state=DISABLED, bg="gray")
        btn_Luu.config(state=DISABLED, bg="gray")
        btn_Huy.config(state=DISABLED, bg="gray")
        btn_Refresh.config(state=DISABLED, bg="gray")

    load_data()
    #load_dichvu_to_combobox()
    dichvu.mainloop()
