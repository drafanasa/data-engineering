'''
    It's your turn!!!

    You will find the directors who won 'Best Director' award in Drama genre
and save their height :)

    Start from this link:
    https://www.imdb.com/search/title/?explore=genres&title_type=feature

    Let's start, you are ready!
'''

# Import các thư viện cần thiết
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import random
import time
import pandas as pd
import openpyxl


# Tạo dict lưu trữ dữ liệu về "director" gồm các key: 'name', 'height_inch', 'height_cm'
director_dict = {
    'director_name': [],
    'director_height_inch': [],
    'director_height_cm': []
}

# Hàm tự động chấp nhận cookie nếu có popup hiển thị
def accept_cookie(the_driver):
    try:
        accept_cookies = the_driver.find_element(By.XPATH, '//button[text()="Accept"]')
        accept_cookies.click()  # Click vào nút Accept
    except:
        pass  # Nếu không tìm thấy popup cookie thì bỏ qua

# Cấu hình options của ChromeDriver trên Win64
service = Service(r"D:\DATA_ENGINEER\Selenium_Driver\chromedriver-win64\chromedriver.exe")
options = Options()

# Thêm User-Agent vào options
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}") 

# Tắt tải hình ảnh bằng cách chỉnh sửa `prefs`
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

options.add_argument("--start-maximized")  # Mở trình duyệt toàn màn hình
options.add_argument("--disable-infobars")  # Tắt thông báo "Chrome is being controlled"
options.add_argument("--disable-popup-blocking")  # Ngăn chặn popup
options.add_argument("--disable-logging")  # Tắt logging không cần thiết
options.add_argument("--log-level=3")  # Giảm mức độ log về mức thấp nhất

options.add_experimental_option("detach", True)  # Giữ trình duyệt mở sau khi script kết thúc

# Khởi tạo WebDriver
driver = webdriver.Chrome(service = service, options = options)

# Truy cập trang đích IMDb
imdb_url = 'https://www.imdb.com/search/title/?explore=genres&title_type=feature'
print(f'\nĐANG TRUY CẬP URL {imdb_url} ...')
driver.get(imdb_url)
time.sleep(3)  # Bắt buộc dừng lại đủ 3s mới cho chạy code tiếp

# Chấp nhận cookie (nếu có)
driver.implicitly_wait(3) # Chờ 3s nếu vẫn chưa tìm thấy phần tử bên dưới
accept_cookie(driver) # Nếu phần tử hiện ra và code này hoạt động trước 3s thì sẽ chạy luôn, không cần chờ
print(f'\n--> Accepting cookies: DONE')

# Chọn thể loại 'Drama' rồi nhấn vào 'Best Director-Winning' trên phàn filter
drama_btn = driver.find_element(By.XPATH, '//span[text()="Drama"]')
drama_btn.click()
print(f'\n--> Chọn thể loại "Drama": DONE')
driver.implicitly_wait(1)
awards_recognition_btn = driver.find_element(By.XPATH,'//div[@id="awardsAccordion"]')
awards_recognition_btn.click()
print(f'\n--> Chọn tab "Awards & recognition": DONE')
driver.implicitly_wait(1)
best_director_winning_btn = driver.find_element(By.XPATH, '//button[@data-testid="test-chip-id-best-director-winning"]') # Dựa vào HTML thực tế, Best Director-Winning nằm trong thẻ <button>, có thuộc tính data-testid="test-chip-id-best-director-winning".
best_director_winning_btn.click()
print(f'\n--> Chọn điều kiện "Best Director-Winning": DONE')
driver.implicitly_wait(3)

# Xử lý pagination - Tìm click nút See more đến khi không còn nút See more thì dừng
print(f'\nĐANG XỬ LÝ PAGINATION SEE MORE ...')
while True:
    time.sleep(2)  # Chờ 2s để trang load
    seemore_buttons = driver.find_elements(By.XPATH, '//span[@class="ipc-see-more__text"]')
        
    if not seemore_buttons:  # Nếu không còn nút "See more", dừng vòng lặp
        print(f'\n--> Không còn nút "See more", xử lý Pagination hoàn tất: DONE')
        break
    
    try:
        seemore_buttons[0].click()  # Click vào nút See more đầu tiên index[0] (phòng trường hợp có nhiều nút See more)
    except Exception as e:
        print(f'\n--> Lỗi: {e}')
        break

# SCRAPING DANH SÁCH MV_LINKS DẪN ĐẾN TRANG THÔNG TIN CỦA TỪNG MOVIE:
print(f'\nĐANG LẤY DANH SÁCH MV_LINKS ...')

# Tạo danh sách rỗng 'mv_links'
mv_links = []
    
# Xác định vị trí HTML chứa tất cả movies
mv_list = driver.find_elements(By.XPATH, '//div[@class="ipc-page-grid__item ipc-page-grid__item--span-2"]/ul/li') # Tìm và lấy danh sách tất cả thẻ li bên trong thẻ ul bên trong div có class="ipc-page-grid__item ipc-page-grid__item--span-2"
    
# Lặp qua từng mv trong mv_list để lấy mv_href --> add vào danh sách mv_links
for mv in mv_list:
    try:
        mv_href = mv.find_element(By.XPATH, './/a[@class="ipc-title-link-wrapper"]').get_attribute('href') # Dùng dấu "." ở trước //tag_name[@class='class_name'] để buộc find_element chỉ được tìm kiếm trong phạm vi của mv thay thì tìm trên toàn trang web
        print(f'\n--> Đang lấy movie_link {mv_href}')
        mv_links.append(mv_href)
        print(f'\n----> DONE')
    except Exception as e:
        print(f'\n--> Lỗi: {e}')
        pass

# Loại bỏ các link trùng lặp trong danh sách mv_links:
mv_links_set = set(mv_links)

# SCRAPING DANH SÁCH DIRECTOR PAGES DẪN ĐẾN TRANG THÔNG TIN CỦA TỪNG DIRECTOR:
print(f'\nĐANG LẤY DANH SÁCH DIRECTOR_PAGES ...')

# Tạo danh sách rỗng director_pages
director_pages = []

# Tạo bộ đếm tiến độ hoàn thành:
count_total = len(mv_links_set)
count_current = 1

# Truy cập từng link trong mv_links_set để lấy director_href --> add vào danh sách director_pages:
for link in mv_links_set:
    time.sleep(random.uniform(0.15, 0.5)) # Thêm độ trễ ngẫu nhiên từ 0.15 đến 0.5 giây để giảm tải thời gian chờ cho vòng lặp
    driver.get(link)

    try:
        print(f'\n--> Đang lấy director_page từ mv_link {link}')
        director_href = driver.find_element(By.XPATH, '(//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"])[1]').get_attribute('href') # Tìm và chọn thẻ a đầu tiên [1] có class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link" để lấy director_href
        director_pages.append(director_href)
        print(f'\n----> DONE [{count_current} / {count_total}]')
        count_current +=1
    except Exception as e:
        print(f'\n--> Lỗi: {e}')
        pass

# Loại bỏ các link trùng lặp trong danh sách director_pages:
director_pages_set = set(director_pages)

# SCRAPING DANH SÁCH DIRECTOR BIOS DẪN ĐẾN TRANG BIOGRAPHY CỦA TỪNG DIRECTOR:
print(f'\nĐANG LẤY DANH SÁCH DIRECTOR_BIOS ...')

# Tạo danh sách rỗng director_bios
director_bios = []

# Reset bộ đếm tiến độ hoàn thành:
count_total = len(director_pages_set)
count_current = 1

# Truy cập từng link trong director_pages_set để lấy bio_href --> add vào danh sách director_bios:
for page in director_pages_set:
    time.sleep(random.uniform(0.15, 0.5)) # Thêm độ trễ ngẫu nhiên từ 0.15 đến 0.5 giây để giảm tải thời gian chờ cho vòng lặp
    driver.get(page)

    try:
        print(f'\n--> Đang lấy director_bio từ director_page {page}')
        bio_href = driver.find_element(By.XPATH, '//a[@class="ipc-overflowText-overlay bio-overflowtext-overlay"]').get_attribute('href') # Như trên
        director_bios.append(bio_href)
        print(f'\n----> DONE [{count_current} / {count_total}]')
        count_current +=1
    except Exception as e:
        print(f'\n--> Lỗi: {e}')
        pass

# Loại bỏ các link trùng lặp trong danh sách director_pages:
director_bios_set = set(director_bios)

# Reset bộ đếm tiến độ hoàn thành:
count_total = len(director_bios_set)
count_current = 1

# SCRAPING DỮ LIỆU VỀ TỪNG DIRECTOR:
print(f'\nĐANG LẤY DỮ LIỆU DIRECTOR BIOGRAPHY ...')
    
# Truy cập từng link trong director_bios_set để lấy data về "director" gồm các key: 'name', 'height_inch', 'height_cm'
if director_bios_set: # Điều kiện này giúp tránh lỗi khi director_bios_set có missing value
    for bio in director_bios_set:
        time.sleep(random.uniform(0.15, 0.5)) # Thêm độ trễ ngẫu nhiên từ 0.15 đến 0.5 giây để giảm tải thời gian chờ cho vòng lặp
        driver.get(bio)
    
        # Khởi tạo giá trị mặc định trước khi dùng try-except
        drt_name = "N/A"
        drt_height_inch = 0
        drt_height_cm = 0

        print(f'\n--> Đang lấy dữ liệu từ director_bio {bio}')
    
        # Tìm vị trí -> lấy data drt_name
        try:
            drt_name = driver.find_element(By.XPATH, '//h2[@class="sc-207b3259-10 kItKVx"]').text
        except:
            pass
        director_dict['director_name'].append(drt_name)
    
        # Tìm vị trí -> Lấy data drt_height_inch và drt_height_cm
        try:
            # Tìm thẻ <span> có text là "Height" -> sibling để tìm div ngay sau nó -> div con -> div cháu là nơi chứa height_text
            height_text = driver.find_element(By.XPATH, '//span[text()="Height"]/following-sibling::div//div//div').text  
            # Tách đôi chuỗi height_text bằng dấu '('
            parts = height_text.split("(") 
            # Lấy inch (trước dấu '(')
            drt_height_inch = parts[0].strip()
            # Lấy cm (sau dấu '('), đồng thời loại bỏ dấu ')'
            drt_height_m = parts[1].replace(" m)", "").strip()
            try:
                drt_height_cm = float(drt_height_m) * 100
            except ValueError:
                drt_height_cm = 0
        except:
            pass
        director_dict['director_height_inch'].append(drt_height_inch)
        director_dict['director_height_cm'].append(drt_height_cm)
        print(f'\n----> DONE [{count_current} / {count_total}]')
        count_current +=1

# Chuyển đổi dữ liệu trong laptop_dict thành một dataframe với Pandas
print('\nBẮT ĐẦU XUẤT FILE DATASET...')
df = pd.DataFrame(director_dict)

# Khởi tạo thư mục output nếu chưa tồn tại
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)  # Tạo folder output

# Lưu dữ dataset vào file CSV trong thư mục `output/`
if df.empty:
    print("\nKhông có dữ liệu để lưu.")
else:
    exported_file_path = os.path.join(output_folder, 'director_data.xlsx')
    df.to_excel(exported_file_path, index=False)
    print(f"\nHoàn thành! Dữ liệu đã được lưu vào {exported_file_path}")

