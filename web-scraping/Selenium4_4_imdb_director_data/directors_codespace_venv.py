# Import các thư viện cần thiết
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # Dùng webdriver-manager để tự động tải ChromeDriver phù hợp với phiên bản Chrome và môi trường linux64 của Codespace Github
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


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
options = Options()

# Thêm User-Agent vào options
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}") 

# Tắt tải hình ảnh bằng cách chỉnh sửa `prefs`
#prefs = {"profile.managed_default_content_settings.images": 2}
#options.add_experimental_option("prefs", prefs)

options.binary_location = "/usr/bin/google-chrome"  # Đường dẫn Chrome trên Linux
options.add_argument("--no-sandbox")  # Cần thiết cho môi trường không có GUI như Codespace
options.add_argument("--disable-dev-shm-usage")  # Giúp tránh lỗi bộ nhớ khi chạy trên container
options.add_argument("--headless=chrome")  # Giữ Chrome chạy giống bình thường nhưng không hiển thị giao diện
options.add_argument("--window-size=1920,1080")  # Đặt kích thước cửa sổ lớn để tránh lỗi layout
options.add_argument("--disable-gpu")  # Chạy mượt hơn khi headless
options.add_argument("--disable-popup-blocking")  # Ngăn chặn popup
options.add_argument("--disable-logging")  # Tắt logging không cần thiết
options.add_argument("--log-level=3")  # Giảm mức độ log về mức thấp nhất

# Khởi tạo WebDriver
service = Service(ChromeDriverManager().install())  # Đảm bảo sử dụng ChromeDriverManager ở đây (thay cho việc dùng path dẫn đến ChromeDriver.exe khi chạy trên môi trường win64 của PC)
driver = webdriver.Chrome(service=service, options=options)
actions = ActionChains(driver)

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

# Dùng WebDriverWait để chờ và ActionChains để click (tránh lỗi chặn):
drama_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Drama"]')))
actions.move_to_element(drama_btn).click().perform()

print(f'\n--> Chọn thể loại "Drama": DONE')

awards_recognition_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="awardsAccordion"]')))
actions.move_to_element(awards_recognition_btn).click().perform()

print(f'\n--> Chọn tab "Awards & recognition": DONE')

time.sleep(3)
best_director_winning_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="test-chip-id-best-director-winning"]')))
actions.move_to_element(best_director_winning_btn).click().perform()

print(f'\n--> Chọn điều kiện "Best Director-Winning": DONE')

# Xử lý pagination - Tìm click nút See more đến khi không còn nút See more thì dừng
print(f'\nĐANG XỬ LÝ PAGINATION SEE MORE ...')
while True:
    time.sleep(2)  # Chờ trang load
    
    try:
        # Tìm tất cả các nút "See more"
        seemore_buttons = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="ipc-see-more__text"]')))
        
        # Nếu không còn nút "See more", thoát vòng lặp
        if not seemore_buttons:
            print(f'\n--> Không còn nút "See more", xử lý Pagination hoàn tất: DONE')
            break

        # Cuộn xuống nút "See more" trước khi click
        driver.execute_script("arguments[0].scrollIntoView(true);", seemore_buttons[0])
        time.sleep(1)  # Chờ sau khi cuộn
        
        # Click vào nút "See more" đầu tiên
        seemore_buttons[0].click()

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
output_folder = '/workspaces/data-engineer-portfolio/web-scraping/Selenium4_4_imdb_director_data/'
os.makedirs(output_folder, exist_ok=True)  # Tạo folder output

# Lưu dữ dataset vào file CSV trong thư mục `output/`
if df.empty:
    print("\nKhông có dữ liệu để lưu.")
else:
    exported_file_path = os.path.join(output_folder, 'director_data.xlsx')
    df.to_excel(exported_file_path, index=False)
    print(f"\nHoàn thành! Dữ liệu đã được lưu vào {exported_file_path}")