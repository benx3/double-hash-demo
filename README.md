# Hệ thống Quản lý Sản phẩm với Double Hashing

Dự án demo về cấu trúc dữ liệu Hash Table sử dụng kỹ thuật Double Hashing để giải quyết va chạm (collision resolution), áp dụng vào hệ thống quản lý danh sách sản phẩm.

## 🚀 Tính năng

- ✅ Thêm sản phẩm với thông tin đầy đủ (mã, tên, giá, số lượng, mô tả)
- 🔍 Tìm kiếm sản phẩm theo mã sản phẩm
- 🗑️ Xóa sản phẩm (lazy deletion)
- 📊 Hiển thị trực quan Hash Table với color coding
- 💾 Lưu trữ dữ liệu vào JSON file
- 📈 Thống kê: load factor, số va chạm, trạng thái bảng
- 🔍 Hiển thị chuỗi thăm dò (probe sequence) cho mỗi thao tác

## 🏗️ Cấu trúc dự án

```
double-hash/
├── app.py                 # Streamlit web application
├── models.py              # Product và HashEntry models
├── double_hashing.py      # DoubleHashTable implementation
├── database.py            # JSON database manager
├── requirements.txt       # Python dependencies
├── products_db.json       # Database file (tự động tạo)
└── README.md             # Documentation
```

## 📦 Cài đặt

### Yêu cầu
- Python 3.8 trở lên

### Các bước cài đặt

1. Clone hoặc tải project về máy

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

## 📘 Hướng dẫn sử dụng

### 1. Tạo Hash Table
- Ở sidebar, nhập kích thước Hash Table (nên chọn số nguyên tố)
- Click "Tạo mới" để khởi tạo

### 2. Thêm sản phẩm
- Chuyển sang tab "➕ Thêm sản phẩm"
- Điền thông tin: Mã SP, Tên, Giá, Số lượng, Mô tả
- Click "Thêm sản phẩm"
- Hệ thống sẽ hiển thị vị trí lưu và chuỗi thăm dò

### 3. Tìm kiếm
- Chuyển sang tab "🔍 Tìm kiếm"
- Nhập mã sản phẩm
- Xem kết quả và chuỗi thăm dó

### 4. Xóa sản phẩm
- Chuyển sang tab "🗑️ Xóa sản phẩm"
- Nhập mã sản phẩm cần xóa
- Sản phẩm sẽ được đánh dấu "deleted" (lazy deletion)

### 5. Xem danh sách
- Tab "📋 Danh sách" hiển thị tất cả sản phẩm còn hoạt động

## 🔬 Double Hashing Algorithm

### Hash Functions

1. **Hash Function 1 (Primary):**
   ```
   h1(key) = sum(ASCII values) mod table_size
   ```

2. **Hash Function 2 (Secondary):**
   ```
   h2(key) = R - (sum(ASCII values) mod R)
   ```
   Trong đó R là số nguyên tố lớn nhất < table_size

3. **Probe Function:**
   ```
   h(key, i) = (h1(key) + i * h2(key)) mod table_size
   ```
   Trong đó i = 0, 1, 2, ...

### Ưu điểm Double Hashing
- Giảm clustering hiệu quả hơn Linear Probing
- Phân bố đều hơn so với Quadratic Probing
- Tận dụng tốt không gian bảng băm

## 💾 Cấu trúc Database

File `products_db.json` lưu trữ:
```json
{
  "size": 11,
  "count": 3,
  "collision_count": 2,
  "table": [
    {
      "product": {
        "ma_san_pham": "SP001",
        "ten_san_pham": "Laptop Dell",
        "gia": 15000000,
        "so_luong": 10,
        "mo_ta": "Laptop gaming"
      },
      "is_deleted": false
    },
    null,
    ...
  ]
}
```

## 🎨 Giao diện

- **Xanh lá**: Ô đã sử dụng (occupied)
- **Cam**: Ô đã xóa (deleted)
- **Xám**: Ô trống (empty)

## 📊 Thống kê

Ứng dụng hiển thị:
- **Kích thước**: Tổng số slot trong bảng
- **Đã sử dụng**: Số slot đang chứa dữ liệu
- **Load Factor**: Tỉ lệ lấp đầy (occupied/size)
- **Số va chạm**: Tổng số collision đã xảy ra

## 🛠️ Technical Stack

- **Streamlit**: Web framework
- **Pandas**: Data display
- **Python dataclasses**: Data models
- **JSON**: Data persistence

## 📝 Lưu ý

- Nên chọn kích thước bảng là số nguyên tố để giảm va chạm
- Load factor > 0.7 có thể ảnh hưởng performance
- Sử dụng lazy deletion để tránh phá vỡ chuỗi thăm dò
- Database tự động lưu sau mỗi thao tác thêm/xóa

## 👨‍💻 Author

Đồ án Giải thuật Nâng cao - Hashing & Double Hashing

---

**Happy Hashing! 🎉**
