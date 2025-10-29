import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root", # thay bằng user MySQL của bạn
        password="150805", # thay bằng password MySQL của bạn
        database="QLKS"
 )
# ===== Kiểm tra kết nối =====
if __name__ == "__main__":
    try:
        conn = connect_db()
        if conn.is_connected():
            print("✅ Kết nối MySQL thành công!")
        conn.close()
    except Exception as e:
        print("❌ Lỗi kết nối MySQL:", e)


