
import time
import schedule
import pytesseract
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import cv2
import numpy as np
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/[username]/traffic-fine-checker.git
git push -u origin main

# Cấu hình Tesseract OCR (thay đổi đường dẫn phù hợp với máy bạn)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def check_traffic_fine():
    try:
        # Khởi tạo trình duyệt Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Chạy ẩn trình duyệt
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Truy cập trang tra cứu
        print("Đang truy cập website CSGT...")
        driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm")
        time.sleep(3)
        
        # Nhập thông tin biển số xe
        print("Đang nhập biển số xe...")
        license_plate = driver.find_element(By.ID, "BienSo")
        license_plate.clear()
        license_plate.send_keys("92D1-92.632632")  # Thay bằng biển số thực
        
        # Chọn loại phương tiện
        print("Đang chọn loại phương tiện...")
        vehicle_type = Select(driver.find_element(By.ID, "LoaiPhuongTien"))
        vehicle_type.select_by_visible_text("Ô tô")
        time.sleep(1)
        
        # Xử lý CAPTCHA
        print("Đang xử lý CAPTCHA...")
        captcha_element = driver.find_element(By.ID, "CaptchaImage")
        captcha_screenshot = captcha_element.screenshot_as_png
        
        # Chuyển đổi ảnh CAPTCHA
        img = Image.open(BytesIO(captcha_screenshot))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Xử lý ảnh để nhận dạng tốt hơn
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Nhận dạng văn bản từ ảnh
        captcha_text = pytesseract.image_to_string(thresh, 
                                                 config='--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        captcha_text = ''.join(e for e in captcha_text if e.isalnum())
        print(f"CAPTCHA nhận dạng được: {captcha_text}")
        
        # Nhập CAPTCHA
        captcha_input = driver.find_element(By.ID, "CaptchaInputText")
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)
        time.sleep(1)
        
        # Thực hiện tra cứu
        print("Đang thực hiện tra cứu...")
        search_button = driver.find_element(By.ID, "btnSearch")
        search_button.click()
        time.sleep(5)
        
        # Lấy kết quả
        result = driver.find_element(By.ID, "grdDanhSachViPham")
        if "Không tìm thấy" in result.text:
            print("✅ Không có vi phạm nào được ghi nhận")
        else:
            print("⚠️ Phát hiện vi phạm:")
            print(result.text)
            
            # Lưu kết quả
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"ket_qua_phat_nguoi_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result.text)
            print(f"Đã lưu kết quả vào file: {filename}")
        
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {str(e)}")
    finally:
        driver.quit()
        print("Hoàn tất quy trình tra cứu\n")

# Lập lịch chạy
schedule.every().day.at("06:00").do(check_traffic_fine)
schedule.every().day.at("12:00").do(check_traffic_fine)

if __name__ == "__main__":
    print("🚔 Bắt đầu chương trình tra cứu phạt nguội tự động")
    print("Lịch chạy: 6:00 và 12:00 hàng ngày\n")
    
    # Chạy ngay lần đầu tiên
    check_traffic_fine()
    
    # Giữ chương trình chạy
    while True:
        schedule.run_pending()
        time.sleep(1)