-- ==============================================
-- TẠO CƠ SỞ DỮ LIỆU QUẢN LÝ KHÁCH SẠN
-- ==============================================
CREATE DATABASE IF NOT EXISTS QLKS;
USE QLKS;
DROP DATABASE QLKS;

-- ==============================================
-- BẢNG NHÂN VIÊN
-- ==============================================
CREATE TABLE NHANVIEN (
    MaNV CHAR(10) PRIMARY KEY,
    HoTenNV VARCHAR(50),
    GioiTinh VARCHAR(5),
    NgaySinh DATE,
    ChucVu VARCHAR(30)
);

-- ==============================================
-- BẢNG KHÁCH HÀNG
-- ==============================================
CREATE TABLE KHACHHANG (
    MaKH CHAR(10) PRIMARY KEY,
    HoTenKH VARCHAR(50),
    QuocTich VARCHAR(30),
    Sdt VARCHAR(15),
    CCCD VARCHAR(20),
    Email VARCHAR(50)
);

-- ==============================================
-- BẢNG PHÒNG
-- ==============================================
CREATE TABLE PHONG (
    MaPhong CHAR(10) PRIMARY KEY,
    TenPhong VARCHAR(30),
    LoaiPhong VARCHAR(20),
    Gia DECIMAL(12,0),
    TrangThai VARCHAR(20)
);

-- ==============================================
-- BẢNG DỊCH VỤ
-- ==============================================
CREATE TABLE DICHVU (
    MaDV CHAR(10) PRIMARY KEY,
    TenDV VARCHAR(50),
    GiaDV DECIMAL(18,0)
);

-- ==============================================
-- BẢNG ĐẶT PHÒNG
-- ==============================================
CREATE TABLE DATPHONG (
    MaDatPhong CHAR(10) PRIMARY KEY,
    MaKHDatPhong CHAR(10),
    MaPhong CHAR(10),
    NgayDat DATE,
    NgayTra DATE,
    SoLuongKhach INT,
    MaKHKhac VARCHAR(50),
    GhiChu VARCHAR(200),
    FOREIGN KEY (MaKHDatPhong) REFERENCES KHACHHANG(MaKH),
    FOREIGN KEY (MaPhong) REFERENCES PHONG(MaPhong)
);

-- ==============================================
-- BẢNG HOÁ ĐƠN
-- ==============================================
CREATE TABLE HOADON (
    MaHoaDon CHAR(10) PRIMARY KEY,
    MaNVThanhToan CHAR(10),
    MaKH CHAR(10),
    MaPhong CHAR(10),
    MaDVDaDat VARCHAR(100),
    TienPhong DECIMAL(18,2),
    TienDV DECIMAL(18,2),
    TongTien DECIMAL(18,0),
    FOREIGN KEY (MaNVThanhToan) REFERENCES NHANVIEN(MaNV),
    FOREIGN KEY (MaKH) REFERENCES KHACHHANG(MaKH),
    FOREIGN KEY (MaPhong) REFERENCES PHONG(MaPhong)
);

-- ==============================================
-- BẢNG NGƯỜI DÙNG
-- ==============================================
CREATE TABLE NGUOIDUNG (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    TenNguoiDung VARCHAR(30),
    MatKhau VARCHAR(30),
    VaiTro VARCHAR(20),
    MaNV CHAR(10),
    MaKH CHAR(10),
    FOREIGN KEY (MaNV) REFERENCES NHANVIEN(MaNV),
    FOREIGN KEY (MaKH) REFERENCES KHACHHANG(MaKH)
);

-- ==============================================
-- THÊM DỮ LIỆU
-- ==============================================

-- NHÂN VIÊN
INSERT INTO NHANVIEN (MaNV, HoTenNV, GioiTinh, NgaySinh, ChucVu) VALUES
('NV001', 'Phan Lê Vi Thanh', 'Nam', '1990-03-15', 'Lễ tân'),
('NV002', 'Lê Thị Thu Diễm', 'Nữ', '1995-07-22', 'Quản lý'),
('NV003', 'Liên Bỉnh Phát', 'Nam', '1998-11-09', 'Phục vụ'),
('NV004', 'Phạm Thị Bé Liên', 'Nữ', '1992-01-18', 'Thu ngân'),
('NV005', 'Trần Văn Bình', 'Nam', '1999-01-01', 'Thu ngân');

-- PHÒNG
INSERT INTO PHONG (MaPhong, TenPhong, LoaiPhong, Gia, TrangThai) VALUES
('P101', 'Phòng 101', 'Đơn', 500000, 'Đã đặt'),
('P102', 'Phòng 102', 'Đơn', 800000, 'Đã đặt'),
('P103', 'Phòng 103', 'Đơn', 1500000, 'Đã đặt'),
('P104', 'Phòng 104', 'Đơn', 900000, 'Trống'),
('P105', 'Phòng 105', 'Đơn', 500000, 'Trống'),
('P106', 'Phòng 106', 'Đơn', 800000, 'Trống'),
('P201', 'Phòng 201', 'Đôi', 1500000, 'Đã đặt'),
('P202', 'Phòng 202', 'Đôi', 900000, 'Đã đặt'),
('P203', 'Phòng 203', 'Đôi', 500000, 'Đã đặt'),
('P204', 'Phòng 204', 'Đôi', 800000, 'Trống'),
('P301', 'Phòng 301', 'VIP', 1500000, 'Đã đặt'),
('P302', 'Phòng 302', 'VIP', 900000, 'Trống');

-- KHÁCH HÀNG
INSERT INTO KHACHHANG (MaKH, HoTenKH, QuocTich, Sdt, CCCD, Email) VALUES
('KH001', 'Trần Thị Thuý Liễu', 'Việt Nam', '0912345678', '080811033521', 'lieulieu@gmail.com'),
('KH002', 'Nguyễn Chí Hùng', 'Việt Nam', '0987654321', '011811033521', 'hungg@gmail.com'),
('KH003', 'John Smith', 'USA', '0845123456', '080822233521', 'john.smith@gmail.com'),
('KH004', 'Nam Joo Hyuk', 'Hàn Quốc', '0823456789', '080822663521', 'joo_nam@gmail.com'), 
('KH005', 'Park Ji Hoon', 'Hàn Quốc', '0823453389', '011811033521', 'hoonie@gmail.com'),
('KH006', 'Sanemi Shinazugawa', 'Nhật Bản', '0822456789', '080877003521', 'sanemi_sasa@gmail.com'),
('KH007', 'Hamada Asahi', 'Nhật Bản', '0823452589', '080551083521', 'sahihi@gmail.com'), 
('KH008', 'Tom Malfoy', 'Anh', '0113456789', '080444033521', 'tomm@gmail.com'),
('KH009', 'Eren Yeager', 'Anh', '0823456559', '089819033529', 'eren_e@gmail.com'), 
('KH010', 'Tsukishima Kei', 'Nhật Bản', '0823356789', '080091933521', 'keikei@gmail.com'), 
('KH011', 'Kageyama Tobio', 'Nhật Bản', '0823456229', '080877033533', 'toto_chan@gmail.com'), 
('KH012', 'Levi Ackerman', 'Anh', '0823422289', '080571033771', 'levi_vi@gmail.com');

-- DỊCH VỤ
INSERT INTO DICHVU (MaDV, TenDV, GiaDV) VALUES
('DV001', 'Giặt ủi', 50000),
('DV002', 'Đưa đón sân bay', 300000),
('DV003', 'Bữa sáng', 100000),
('DV004', 'Spa & Massage', 500000),
('DV005', 'Trang trí theo yêu cầu', 1000000);

-- ĐẶT PHÒNG
INSERT INTO DATPHONG 
(MaDatPhong, MaKHDatPhong, MaPhong, NgayDat, NgayTra, SoLuongKhach, MaKHKhac, GhiChu) 
VALUES
('DP001', 'KH001', 'P201', '2025-10-25', '2025-10-27', 2, 'KH002', 'Khách yêu cầu phòng gần thang máy' ),
('DP002', 'KH004', 'P101', '2025-10-26', '2025-10-30', 1, NULL, NULL ),
('DP003', 'KH003', 'P102', '2025-10-28', '2025-10-30', 1, NULL, 'Khách nước ngoài' ),
('DP004', 'KH005', 'P103', '2025-10-29', '2025-10-31', 1, NULL, 'Khách yêu cầu phòng view biển' ),
('DP005', 'KH006', 'P202', '2025-10-29', '2025-10-31', 2, 'KH007', 'Khách tổ chức sinh nhật' ),
('DP006', 'KH008', 'P203', '2025-10-29', '2025-10-31', 2, 'KH009', 'Khách muốn checkin sớm'),
('DP007', 'KH010', 'P301', '2025-10-29', '2025-10-31', 3, 'KH011, KH012', 'Nhóm 3 người');


-- HOÁ ĐƠN
INSERT INTO HOADON (MaHoaDon, MaNVThanhToan, MaKH, MaPhong, MaDVDaDat, TienPhong, TienDV, TongTien) VALUES
('HD001', 'NV004', 'KH001', 'P201', 'DV003', 3000000, 100000, 3100000),
('HD002', 'NV005', 'KH004', 'P101', 'DV004', 2000000, 500000, 2500000),
('HD003', 'NV005', 'KH003', 'P102', 'DV003', 1600000, 100000, 1700000),
('HD004', 'NV004', 'KH005', 'P103', 'DV001', 3000000, 50000, 3050000),
('HD005', 'NV004', 'KH006', 'P202', 'DV001', 1800000, 50000, 1850000),
('HD006', 'NV005', 'KH008', 'P203', 'DV001', 1000000, 50000, 1050000),
('HD007', 'NV004', 'KH010', 'P301', 'DV001', 3000000, 50000, 3050000);

-- NGƯỜI DÙNG
INSERT INTO NGUOIDUNG (TenNguoiDung, MatKhau, VaiTro, MaNV, MaKH) VALUES
('ND01', '1111', 'Admin', NULL, NULL),
('ND02', '2222', 'NhanVien', 'NV001', NULL),
('ND03', '3333', 'NhanVien', 'NV002', NULL),
('ND04', '4444', 'Customer', NULL, 'KH001');

SELECT * FROM NHANVIEN;
SELECT * FROM KHACHHANG;
SELECT * FROM PHONG;
SELECT * FROM DICHVU;
SELECT * FROM DATPHONG;
SELECT * FROM HOADON;
SELECT * FROM NGUOIDUNG;







