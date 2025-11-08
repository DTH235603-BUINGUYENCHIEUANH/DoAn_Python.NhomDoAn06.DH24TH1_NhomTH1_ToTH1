import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# === Kết nối MySQL toàn cục ===
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="150805",
            database="QLKS"
        )
        print("✅ Kết nối MySQL thành công!")
        return conn
    except mysql.connector.Error as err:
        print("❌ Lỗi khi kết nối MySQL:", err)
        return None


# === Khởi tạo kết nối một lần ===
conn = connect_db()
if conn:
    cur = conn.cursor()
else:
    cur = None


