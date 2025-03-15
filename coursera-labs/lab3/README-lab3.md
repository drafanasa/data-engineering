# Web Scraping Lab - Book Data Extraction (Static Web)

**`Description:`**
- Lab thuộc khóa **"Complete Python Web Scraping : Real Projects & Modern Tools"** trên Udemy.
- Tập trung vào **Web Scraping** để thu thập data từ một static website mẫu là `books.toscrape.com`

**`Key skills:`**
- Python (Requests, BeautifulSoup, Pandas)
- Jupyter Notebook
- Web Scraping 

---

## Book Data Extraction - Single Book
- Scraping data từ **một đầu sách cụ thể** trên `books.toscrape.com`.
- Các thông tin thu thập bao gồm: tiêu đề sách, giá, tình trạng tồn kho, đánh giá,..

**`Outcome:`**
- Hiểu cách sử dụng **Requests** và **BeautifulSoup** để thu thập data từ một static website.  
- Lưu trữ data thu thập được vào DataFrame và xuất ra file CSV bằng **Pandas**.  

---

## Book Data Extraction - All Books
- Gửi requests đến website `books.toscrape.com` thông qua Proxy/Authenticate.
- Scraping data từ **tất cả các đầu sách** trên tất cả các page của website .
- Thu thập các thông tin như tiêu đề, giá, tình trạng tồn kho, đánh giá,.. cho mỗi đầu sách.
- Lưu trữ data thu thập được vào DataFrame và xuất ra file CSV bằng **Pandas**. 

**`Outcome:`**
- Tự động hóa quá trình thu thập data trên nhiều trang.  
- Tìm, lọc và lấy data mong muốn từ static website.  
- Tối ưu code để tránh bị chặn bởi website và tránh lỗi.  
- Lưu trữ data thu thập được dưới dạng file CSV để phân tích về sau.

---

## Data Extracted:
- **`book_data.csv`**: Dataset về tất cả các đầu sách trên `books.toscrape.com`. 
- **`book_images`**: Hình ảnh tất cả các đầu sách trên `books.toscrape.com`.

---

**`General Outcome:`**
- Dùng **Python Requests** và **BeautifulSoup** thông qua **Proxy/Authenticate** để web scraping.
- Xử lý và phân tích data thu thập được bằng **Pandas** dataframe.
- Lưu trữ data trích xuất được và tối ưu code web scraping. 