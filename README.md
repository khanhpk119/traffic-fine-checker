# 🚔 Traffic Fine Checker

Công cụ tự động tra cứu phạt nguội từ website CSGT Việt Nam

## 📝 Yêu cầu hệ thống
- Python 3.10+
- Chrome browser
- Tesseract OCR 5.0+
- Git

## 🛠️ Cài đặt

1. **Cài đặt phụ thuộc**:
```bash
git clone https://github.com/[username]/traffic-fine-checker.git
cd traffic-fine-checker
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

2. **Cài đặt Tesseract OCR**:
- Windows: [Tải tại đây](https://github.com/UB-Mannheim/tesseract/wiki)
- macOS: `brew install tesseract`
- Linux: `sudo apt install tesseract-ocr tesseract-ocr-vie`

## 🚀 Sử dụng

1. Chỉnh sửa file `traffic_fine_checker.py`:
   - Dòng 14: Đặt đường dẫn Tesseract
   - Dòng 32: Nhập biển số xe cần tra cứu
   - Dòng 36: Chọn loại phương tiện

2. Chạy chương trình:
```bash
python traffic_fine_checker.py
```

3. Chương trình sẽ:
- Tự động chạy ngay lần đầu
- Chạy vào 6h sáng và 12h trưa hàng ngày
- Lưu kết quả vào file text nếu phát hiện vi phạm

## 📂 Cấu trúc dự án
- `traffic_fine_checker.py`: Script chính
- `requirements.txt`: Danh sách thư viện
- `README.md`: Hướng dẫn sử dụng

## ⚠️ Lưu ý
- Đảm bảo máy tính luôn bật để chạy tự động
- Tỷ lệ nhận dạng CAPTCHA có thể không 100% chính xác
- Tuân thủ quy định của website CSGT Việt Nam
