# Import các thư viện cần thiết
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # Dùng webdriver-manager để tự động tải ChromeDriver phù hợp với phiên bản Chrome và môi trường linux64 của Codespace Github
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import random
import time
import pandas as pd
import username_n_password

# Tạo dict rỗng để chứa các data cần scraping gồm: 'author name', 'author birth date' và 'author birth place'
author_data_dict = {
    'author-name':[],
    'author-birth-date':[],
    'author-birth-place':[]
}

# Tạo danh sách rỗng chứa links của các author pages
author_pages = []

# Cấu hình options của ChromeDriver 
options = Options()

# Thêm options User-Agent vào options
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

# Thêm các options tối ưu Selenium 4
options.binary_location = "/usr/bin/google-chrome"  # Đường dẫn Chrome trên Linux
options.add_argument("--no-sandbox")  # Cần thiết cho môi trường không có GUI như Codespace
options.add_argument("--disable-dev-shm-usage")  # Giúp tránh lỗi bộ nhớ khi chạy trên container
options.add_argument("--headless=chrome")  # Giữ Chrome chạy giống bình thường nhưng không hiển thị giao diện
options.add_argument("--window-size=1920,1080")  # Đặt kích thước cửa sổ lớn để tránh lỗi layout
options.add_argument("--disable-gpu")  # Chạy mượt hơn khi headless

# Khởi tạo WebDriver
service = Service(ChromeDriverManager().install())  # Đảm bảo sử dụng ChromeDriverManager ở đây (thay cho việc dùng path dẫn đến ChromeDriver.exe khi chạy trên môi trường win64 của PC)
driver = webdriver.Chrome(service=service, options=options)

# Truy cập url của main page
main_page_url = 'https://quotes.toscrape.com/'
driver.get(main_page_url)

# Tạo function tự động Login với Selenium 4
def auto_login(driver, login_url, username, password):
    try:
        print(f'ĐANG AUTO LOGIN {login_url}')
        # Truy cập login page
        driver.get(login_url) 
        
        # Chờ 3s để load web rồi kiểm tra coi khung nhập username hiện lên chưa, nếu hiện thì mới chạy tiếp code 
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username'))) 

        # Nhập thông tin login rồi submit
        driver.find_element(By.CSS_SELECTOR, '#username').send_keys(username) # Tìm ô có ID 'username' -> nhập username
        driver.find_element(By.CSS_SELECTOR, '#password').send_keys(password) # Tìm ô có ID 'password' -> nhập password
        driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login'].btn.btn-primary").click() # Tìm và click nút Login (HTML nút này là <input type="submit" value="Login" class="btn btn-primary">)

        # Chờ tiếp 3s để load web rồi kiểm tra coi đăng nhập thành công chưa -> nếu nút Logout hiện lên thì mới chạy tiếp code
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/logout"]'))) # HTML nút logout là <a href="/logout">Logout</a>
        print('--> Login thành công!')

    except Exception as e:
        print(f'--> Lỗi: {e}')

# Gọi function auto_login với login_url, username và password
auto_login(driver, 'https://quotes.toscrape.com/login', username_n_password.username, username_n_password.password)

# Tạo vòng lặp While duyệt qua từng page để scraping dữ liệu cần thiết + có xử lý pagination là Next Button
page_no = 1

while True:
    
    # Truy cập page_url
    page_url = f'https://quotes.toscrape.com/page/{page_no}/'
    driver.get(page_url)
    print(f'\nĐANG SCRAPING PAGE {page_no}')

    # Chờ 3s đến khi web load class 'quote' thì chạy code tiếp
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.quote'))) 

    # Xác định vị trí tất cả quotes hiện có trên page
    quotes = driver.find_elements(By.CSS_SELECTOR, '.quote')

    print('\n--> Đang lấy link (about) của từng quote...')
    
    # Thêm độ trễ từ 1 đến 3 giây
    time.sleep(random.uniform(1, 3)) 

    # Tạo vòng lặp For lấy link tác giả (about) của mỗi quote trên page -> gửi vào danh sách author_pages = []
    for quote in quotes:
        try:
            author_span = quote.find_element(By.CSS_SELECTOR, 'span a')
            author_link = author_span.get_attribute('href')
            author_pages.append(author_link)
            print(f'\n------> {author_link}')
            
        except Exception as e:
            print(f'\n-----> Lỗi: {e}')

    # Xử lý Pagination với Next Button:
    try:
        next_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.next a'))) # Cách viết này nghĩa là tìm thẻ <'li' có class '.next'> trước, rồi mới tìm tới thẻ 'a' nằm bên trong nó
        next_btn.click()
        page_no +=1
        time.sleep(random.uniform(1, 3)) # Đợi 1-3s trước khi load tiếp
    except:
        print('\n--> Không còn trang kế tiếp. Hoàn tất scraping.')
        break
        
# Dùng set() để loại bỏ phần tử trùng nhau cho danh sách author_page
author_pages_set = set(author_pages)

# Tạo vòng lặp For duyệt qua từng link trong author_page_set: 
for author_link in author_pages_set:
    try:
        print(f'\nĐANG SCRAPING {author_link}')
        time.sleep(random.uniform(1, 3)) # Thêm độ trễ từ 1 đến 3 giây
        driver.get(author_link) # Truy cập link author_link
    
        # Thu thập các data về author --> add vào data_dict
        # Khởi tạo giá trị mặc định trước khi dùng try-except
        author_name = "N/A"
        author_birth_date = "N/A"
        author_birth_place = "N/A"

        # Dùng try-except để tránh việc data cần lấy không tồn tại --> gây lỗi missing value khi tạo dataset sau này
        # Lấy 'author_name'
        try:
            author_name = driver.find_element(By.CSS_SELECTOR, 'h3.author-title').text # Thẻ h3 class '.author_title'
        except:
            pass
        author_data_dict['author-name'].append(author_name)

        # Lấy 'author_birth_date'
        try:
            author_birth_date = driver.find_element(By.CSS_SELECTOR, 'span.author-born-date').text # Thẻ span class '.author-born-date'
        except: 
            pass
        author_data_dict['author-birth-date'].append(author_birth_date)

        # Lấy 'author_birth_place'
        try:
            author_birth_place = driver.find_element(By.CSS_SELECTOR, 'span.author-born-location').text # Thẻ span class '.author-born-location'
        except:
            pass
        author_data_dict['author-birth-place'].append(author_birth_place)
        
        print(f'\n--> Scraping thành công: {author_name} | {author_birth_date} | {author_birth_place}')
        
    except Exception as e:
        print(f'\n--> Lỗi: {e}')

# Cho author_data_dict vào Pandas dataframe, xuất ra file CSV
print('\nĐANG XUẤT FILE DATASET...')

# Tạo Pandas dataframe từ author_data_dict
df = pd.DataFrame(author_data_dict)

# Khởi tạo thư mục output nếu chưa tồn tại
output_folder = "/workspaces/data-engineer-portfolio/web-scraping/Selenium4_2_author_data/output"
os.makedirs(output_folder, exist_ok=True)

# Lưu dữ dataset vào file CSV trong thư mục `output/`
if df.empty:
    print("\n--> Lỗi: Không có dữ liệu để xuất file.")
else:
    csv_file_path = os.path.join(output_folder, 'author_data.csv')
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f'\n--> Hoàn thành: đã xuất file CSV vào {csv_file_path}')
