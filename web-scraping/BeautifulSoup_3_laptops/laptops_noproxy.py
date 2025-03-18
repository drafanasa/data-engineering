import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# Khởi tạo dictionary trống chứa data cần scrap
laptop_dict = {
    'name': [],
    'price': [],
    'shipping': [],
    'link': []
}
print('\nKHỞI TẠO CHƯƠNG TRÌNH...')

# Khởi tạo thư mục output nếu chưa tồn tại
output_folder = 'output_noproxy'
os.makedirs(output_folder, exist_ok=True)  # Tạo folder output

# Khởi tạo Fake User-Agent để tránh bị chặn
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "DNT": "1",
    "Referer": "https://www.ebay.com/",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
}

# Khởi tạo cookies để tránh bị chặn
cookies = {
    "ebay": "%5Ejs%3D1%5Esbf%3D%23000000%5E",
    "nonsession": "BAQAAAZRXz2gmAAaAADMAAWm6PHg/AMoAIGubb/g4ZmQzMTQ3YzE5NTBhOGNkZjdjMDI4MzFmZmZmZTgzNADLAAJn2RAAMTP+NzAsL+9tsYSVG7bSOk7IiejziQ**",
    "s": "CgADuAJFn2XkcMwZodHRwczovL3d3dy5lYmF5LmNvbS9zY2gvaS5odG1sP19kY2F0PTE3NyZfZnNycD0xJnJ0PW5jJl9mcm9tPVI0MCZSQU0lMjUyMFNpemU9MzIlMjUyMEdCJl9ua3c9bGFwdG9wJl9zYWNhdD0wJlNTRCUyNTIwQ2FwYWNpdHk9MSUyNTIwVEImX3Bnbj0xBwD4ACBn2V2TOGZkMzE0N2MxOTUwYThjZGY3YzAyODMxZmZmZmU4MzQgt8aX",
}

print('\nBẮT ĐẦU SCRAPING...')
page_no = 1  # Bắt đầu scraping từ page 1

while True:
    print(f'Scraping Page --> {page_no}')
    page_url = f'https://www.ebay.com/sch/i.html?_dcat=177&_fsrp=1&rt=nc&_from=R40&RAM%2520Size=32%2520GB&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB&_pgn={page_no}'
    
    try:
        time.sleep(random.uniform(3, 7))  # Thêm độ trễ ngẫu nhiên từ 3 đến 7 giây trước khi gửi requests
        response = requests.get(page_url, headers=headers, timeout=20)
        response.raise_for_status()  # Nếu gặp lỗi HTTP (403, 500, ...) thì raise lỗi
        print(f"Request thành công - Page {page_no}")
    except requests.exceptions.RequestException as e:
        print(f"Request thất bại - Page {page_no}: {e}")
        break
    
    soup = BeautifulSoup(response.text, 'html.parser')
    laptops = soup.find_all('div', class_='s-item__info')
    
    for laptop in laptops:
        name = laptop.find('span', attrs={'role': 'heading'})
        price = laptop.find('span', class_='s-item__price')
        shipping = laptop.find('span', class_='s-item__logisticsCost')
        link = laptop.find('a', class_='s-item__link')
        
        laptop_dict['name'].append(name.text if name else 'No info')
        laptop_dict['price'].append(price.text if price else 'No info')
        laptop_dict['shipping'].append(shipping.text if shipping else 'No info')
        laptop_dict['link'].append(link['href'] if link else 'No info')

    # Code xử lý pagination
    next_as_button = soup.find('button', class_='pagination__next')

    # Dùng code này nếu muốn vòng lặp dừng sau khi scrap xong page đầu tiên, chỉ để test cho nhanh
    if next_as_button is None:
        break

    # Dùng code này nếu muốn vòng lặp dừng sau khi scrap xong TẤT CẢ CÁC PAGE có data sản phẩm
    #if next_as_button is not None or next_as_button.get('aria-disabled') == 'true': # Kiểm tra nếu nút 'Next' bị vô hiệu hóa hoặc không tồn tại
    #   print("✅ Không còn trang tiếp theo. Kết thúc scraping.")
    #    break

    page_no += 1

print('\nBẮT ĐẦU XUẤT FILE DATASET...')
df = pd.DataFrame(laptop_dict)

if df.empty:
    print("Không có dữ liệu để lưu.")
else:
    csv_file_path = os.path.join(output_folder, 'laptop_data_noproxy.csv')
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
    print(f'Hoàn thành: xuất file CSV vào {csv_file_path}')