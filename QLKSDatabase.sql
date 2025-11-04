-- ==============================================
-- TẠO CƠ SỞ DỮ LIỆU QUẢN LÝ KHÁCH SẠN
-- ==============================================
CREATE DATABASE IF NOT EXISTS QLKS;
USE QLKS;

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
    Gia DECIMAL(18,2),
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
DROP TABLE DATPHONG;
CREATE TABLE DATPHONG (
    MaDatPhong CHAR(10) PRIMARY KEY,
    MaKHDatPhong CHAR(10),
    MaPhong CHAR(10),
    NgayDat DATE,
    NgayTra DATE,
    SoNgayO INT,
    SoLuongKhach INT,
    MaKHKhac VARCHAR(50),
    ThanhTien DECIMAL(18,2),
    GhiChu VARCHAR(200),
    FOREIGN KEY (MaKHDatPhong) REFERENCES KHACHHANG(MaKH),
    FOREIGN KEY (MaPhong) REFERENCES PHONG(MaPhong)
);

-- ==============================================
-- BẢNG ĐẶT DỊCH VỤ
-- ==============================================
CREATE TABLE DATDICHVU (
    MaDatDV CHAR(10) PRIMARY KEY,
    MaKHDatDV CHAR(10),
    MaDV CHAR(10),
    SoLuongDV INT,
    ThanhTien DECIMAL(18,2),
    FOREIGN KEY (MaKHDatDV) REFERENCES KHACHHANG(MaKH),
    FOREIGN KEY (MaDV) REFERENCES DICHVU(MaDV)
);


-- ==============================================
-- BẢNG HOÁ ĐƠN
-- ==============================================
CREATE TABLE HOADON (
    MaHoaDon CHAR(10) PRIMARY KEY,
    MaNVThanhToan CHAR(10),
    MaKH CHAR(10),
    PhuongThucTT VARCHAR(50) CHECK (PhuongThucTT IN ('Chuyen khoan','Tien mat')),
    TongTien DECIMAL(18,2),
    FOREIGN KEY (MaNVThanhToan) REFERENCES NHANVIEN(MaNV),
    FOREIGN KEY (MaKH) REFERENCES KHACHHANG(MaKH)
);

-- ==============================================
-- BẢNG NGƯỜI DÙNG
-- ==============================================
DROP TABLE NGUOIDUNG;
CREATE TABLE NGUOIDUNG (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    TenNguoiDung VARCHAR(30),
    MatKhau VARCHAR(30),
    MaNV CHAR(10),
    FOREIGN KEY (MaNV) REFERENCES NHANVIEN(MaNV)
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
(MaDatPhong, MaKHDatPhong, MaPhong, NgayDat, NgayTra, SoNgayO, SoLuongKhach, MaKHKhac, ThanhTien, GhiChu) 
VALUES
-- DP001: KH001 đặt phòng đôi P201 (1.500.000/đêm) ở 2 đêm → 3.000.000
('DP001', 'KH001', 'P201', '2025-10-25', '2025-10-27', 2, 2, 'KH002', 3000000, 'Khách yêu cầu phòng gần thang máy'),
-- DP002: KH004 đặt phòng đơn P101 (500.000/đêm) ở 4 đêm → 2.000.000
('DP002', 'KH004', 'P101', '2025-10-26', '2025-10-30', 4, 1, NULL, 2000000, NULL),
-- DP003: KH003 đặt phòng đơn P102 (800.000/đêm) ở 2 đêm → 1.600.000
('DP003', 'KH003', 'P102', '2025-10-28', '2025-10-30', 2, 1, NULL, 1600000, 'Khách nước ngoài'),
-- DP004: KH005 đặt phòng đơn P103 (1.500.000/đêm) ở 2 đêm → 3.000.000
('DP004', 'KH005', 'P103', '2025-10-29', '2025-10-31', 2, 1, NULL, 3000000, 'Khách yêu cầu phòng view biển'),
-- DP005: KH006 đặt phòng đôi P202 (900.000/đêm) ở 6 đêm → 5.400.000
('DP005', 'KH006', 'P202', '2025-10-25', '2025-10-31', 6, 2, 'KH007', 5400000, 'Khách tổ chức sinh nhật'),
-- DP006: KH008 đặt phòng đôi P203 (500.000/đêm) ở 5 đêm → 2.500.000
('DP006', 'KH008', 'P203', '2025-10-25', '2025-10-30', 5, 2, 'KH009', 2500000, 'Khách muốn checkin sớm'),
-- DP007: KH010 đặt phòng VIP P301 (1.500.000/đêm) ở 2 đêm → 3.000.000
('DP007', 'KH010', 'P301', '2025-10-29', '2025-10-31', 2, 3, 'KH011, KH012', 3000000, 'Nhóm 3 người');

-- ĐẶT DỊCH VỤ 
INSERT INTO DATDICHVU (MaDatDV, MaKHDatDV, MaDV, SoLuongDV, ThanhTien) VALUES
-- KH001: sử dụng Bữa sáng (DV003) cho 2 người × 2 ngày = 4 phần
('DVU001', 'KH001', 'DV003', 4, 400000),
-- KH003: chỉ dùng Bữa sáng 2 phần
('DVU002', 'KH003', 'DV003', 2, 200000),
-- KH004: sử dụng Spa & Massage 1 lần
('DVU003', 'KH004', 'DV004', 1, 500000),
-- KH004: sử dụng Đưa đón sân bay 1 lần
('DVU004', 'KH004', 'DV002', 1, 300000),
-- KH005: sử dụng Giặt ủi 3 lần
('DVU005', 'KH005', 'DV001', 3, 150000),
-- KH006: đặt Trang trí theo yêu cầu (sinh nhật) 1 lần
('DVU006', 'KH006', 'DV005', 1, 1000000),
-- KH006: thêm Bữa sáng cho 2 người × 2 ngày = 4 phần
('DVU007', 'KH006', 'DV003', 4, 400000),
-- KH008: chỉ sử dụng Giặt ủi 2 lần
('DVU008', 'KH008', 'DV001', 2, 100000),
-- KH010: dùng Spa & Massage 2 lần (VIP khách)
('DVU009', 'KH010', 'DV004', 2, 1000000),
-- KH010: dùng Giặt ủi 3 lần (VIP khách)
('DVU010', 'KH010', 'DV001', 3, 150000),
-- KH010: thêm Trang trí theo yêu cầu (phòng VIP)
('DVU011', 'KH010', 'DV005', 1, 1000000);

-- HOÁ ĐƠN
INSERT INTO HOADON (MaHoaDon, MaNVThanhToan, MaKH, PhuongThucTT, TongTien) VALUES
('HD001', 'NV004', 'KH001', 'Chuyen khoan', 3400000),                 
('HD002', 'NV005', 'KH004', 'Chuyen khoan', 2800000),
('HD003', 'NV005', 'KH003', 'Tien mat', 1800000),
('HD004', 'NV004', 'KH005', 'Chuyen khoan', 3150000),
('HD005', 'NV004', 'KH006', 'Tien mat', 6800000),
('HD006', 'NV005', 'KH008', 'Tien mat', 2600000),
('HD007', 'NV004', 'KH010', 'Chuyen khoan', 5150000);

-- NGƯỜI DÙNG
INSERT INTO NGUOIDUNG (TenNguoiDung, MatKhau, MaNV) VALUES
('ND01', '1111', 'NV004'),
('ND02', '2222', 'NV001'),
('ND03', '3333', 'NV002');

SELECT * FROM NHANVIEN;
SELECT * FROM KHACHHANG;
SELECT * FROM PHONG;
SELECT * FROM DICHVU;
SELECT * FROM DATPHONG;
SELECT * FROM HOADON;
SELECT * FROM NGUOIDUNG;







