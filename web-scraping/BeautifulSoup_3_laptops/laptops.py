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
output_folder = 'output'
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

# Đọc danh sách proxy từ file proxy_list.txt và loại bỏ dòng trống
with open('/workspaces/data-engineer-portfolio/web-scraping/BeautifulSoup_3_laptops/proxy_list.txt', 'r') as p:
    proxy_list = [proxy.strip() for proxy in p if proxy.strip()]

# Khởi tạo danh sách chứa các proxy đang hoạt động
working_proxies = [] 

# Thiết lập url mặc định để test proxies
test_proxy_url = 'https://www.ebay.com'

print('\nBẮT ĐẦU TEST PROXY...')
# Lặp qua từng proxy để gửi request
for proxy in proxy_list:
    my_proxy = proxy
    proxy_url = f"http://{my_proxy}"  # Tạo URL của proxy

    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }

    # Thiết lập try-except nâng cao để kiểm tra trạng thái và xử lý lỗi
    try:
        time.sleep(random.uniform(3, 7)) # Thêm độ trễ từ 0.05 đến 0.3 giây trước khi gửi requests (thời gian ngắn để giảm tải cho quá trình test proxy)
        response = requests.get(test_proxy_url, proxies=proxies, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        response.raise_for_status() # Nếu gặp lỗi HTTP (403, 500, ...) thì raise lỗi
        # Kiểm tra kết quả
        if response.status_code == 200:
            print(f'Request thành công. Proxy: {proxy} - Đã thêm vào danh sách các proxy đang hoạt động')
            working_proxies.append(proxy)
        else:
            print(f'Request thất bại. Proxy: {proxy} - Mã trạng thái: {response.status_code}')

    except requests.exceptions.ProxyError: # Xử lý lỗi proxy không hoạt động
        print(f'Proxy lỗi: {proxy}. Thử proxy khác...')

    except requests.exceptions.ConnectTimeout: # Xử lý lỗi timeout khi proxy quá chậm
        print(f'Proxy quá chậm: {proxy}. Bỏ qua...')

    except requests.exceptions.ConnectionError: # Xử lý lỗi khi proxy không thể kết nối đến server
        print(f'Không thể kết nối: {proxy}. Thử proxy khác...')

    except requests.exceptions.HTTPError as err: # Xử lý lỗi HTTP khác (403, 404, 500,...)
        print(f'HTTP Error: {err}')

    except Exception as e: # Xử lý các lỗi khác không xác định
        print(f'Lỗi khác: {e}')
        
# Khởi tạo dictionary để đếm lỗi của từng proxy
proxy_errors = {proxy: 0 for proxy in working_proxies}

# Xử lý nếu working_proxies rỗng trước khi chạy vòng lặp scraping để tránh lỗi vào scrap mà không có proxy khả dụng
if not working_proxies:
    print('Không có proxy nào hoạt động, dừng scraping.')
    exit()
    
print('\nBẮT ĐẦU SCRAPING...')
page_no = 1 # Bắt đầu scraping từ page 1
max_retry = min(5, len(working_proxies))  # Số lần thử lại tối đa với proxy khác, điều chỉnh max_retry động dựa trên số proxy khả dụng

while True:
    print(f'Scraping Page --> {page_no}')
    page_url = f'https://www.ebay.com/sch/i.html?_dcat=177&_fsrp=1&rt=nc&_from=R40&RAM%2520Size=32%2520GB&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB&_pgn={page_no}'
    
    # Luân chuyển proxy và gửi requests
    for attempt in range(max_retry):
        proxy = random.choice(working_proxies)  # Chọn ngẫu nhiên proxy nào đó trong danh sách working_proxies đã test thành công
        proxies = {
            "http": f"http://{proxy}", 
            "https": f"http://{proxy}"
        }
        
        try:
            time.sleep(random.uniform(3, 7)) # Thêm độ trễ ngẫu nhiên từ 3 đến 7 giây trước khi gửi requests
            response = requests.get(page_url, proxies=proxies, headers=headers, timeout=20)
            if response.status_code == 200:
                print(f"Request thành công với proxy: {proxy}")
                proxy_errors[proxy] = 0  # Reset số lỗi cho proxy này nếu request thành công
                break  # Thoát vòng lặp nếu thành công
            else:
                print(f"Request thất bại với proxy: {proxy} - Status: {response.status_code}")
                proxy_errors[proxy] += 1
        except:
            print(f"Proxy lỗi trong scraping: {proxy}")
            proxy_errors[proxy] += 1
            
        # Cơ chế loại bỏ proxy nếu lỗi 3 lần liên tiếp + cho break ngay vòng lặp for nếu danh sách working_proxies trở nên rỗng trong quá trình scraping
        if proxy_errors[proxy] >= 3:
            print(f"Proxy {proxy} lỗi 3 lần liên tiếp, loại khỏi danh sách.")
            working_proxies.remove(proxy)
            del proxy_errors[proxy]
            if not working_proxies:
                print("Không còn proxy hoạt động, dừng scraping.")
                break
                
    if response.status_code != 200:
        continue # Khi continue chạy, Python sẽ bỏ qua tất cả phần code còn lại trong vòng lặp While hiện tại và chuyển ngay sang lần lặp tiếp theo.

    soup = BeautifulSoup(response.text, 'html.parser')
    
    laptops = soup.find_all('div', class_='s-item__info')
    
    for laptop in laptops:
        
        # Lấy name - nếu không có thì trả về giá trị 'No info' để tránh missing value
        if laptop.find('span', attrs={'role': 'heading'}) is not None:
            name = laptop.find('span', attrs={'role': 'heading'}).text
            laptop_dict['name'].append(name)
            print(name)
        else:
            name = 'No info'
            laptop_dict['name'].append(name)
            print(name)

        # Lấy price - nếu không có thì trả về giá trị 'No info' để tránh missing value
        if laptop.find('span', class_='s-item__price') is not None:
            price = laptop.find('span', class_='s-item__price').text
            laptop_dict['price'].append(price)
            print(price)
        else:
            price = 'No info'
            laptop_dict['price'].append(price)
            print(price)
        
        # Lấy shipping - nếu không có thì trả về giá trị 'No info' để tránh missing value
        if laptop.find('span', class_='s-item__logisticsCost') is not None:
            shipping = laptop.find('span', class_='s-item__logisticsCost').text
            laptop_dict['shipping'].append(shipping)
            print(shipping)
        else:
            shipping = 'No info'
            laptop_dict['shipping'].append(shipping)
            print(shipping)

        # Lấy link - nếu không có thì trả về giá trị 'No info' để tránh missing value
        if laptop.find('a', class_='s-item__link') is not None:
            link = laptop.find('a', class_='s-item__link')['href']
            laptop_dict['link'].append(link)
            print(link)
        else:
            link = 'No info'
            laptop_dict['link'].append(link)
            print(link)

    
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
# Chuyển đổi dữ liệu trong laptop_dict thành một dataframe với pandas
df = pd.DataFrame(laptop_dict)

# Lưu dữ dataset vào file CSV trong thư mục `output/`
if df.empty:
    print("Không có dữ liệu để lưu.")
else:
    csv_file_path = os.path.join(output_folder, 'laptop_data.csv')
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
    print('Hoàn thành: xuất file CSV vào {csv_file_path}')
