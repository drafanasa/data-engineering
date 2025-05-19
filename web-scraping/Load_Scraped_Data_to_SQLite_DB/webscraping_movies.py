import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd

# KHAI BÁO THỰC THỂ ======================================================================================
url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = '/home/project/Web_Scraping_Movies_IBM_Course/top_50_films.csv'
my_df = pd.DataFrame(columns=["Average Rank","Film","Year"])
count = 0

# TẢI TRANG WEB CẦN SCRAP BẰNG THƯ VIỆN REQUEST VÀ BEAUTIFULSOUP =========================================
html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

# KIỂM TRA HTML TRÊN WEB -> XÁC ĐỊNH DATA CẦN SCRAP -> CHẠY VÒNG LẶP SỬ DỤNG CÁC SELECTOR ĐỂ LẤY DATA ====
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')
for row in rows:
    if count<50:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {"Average Rank": col[0].contents[0],
                         "Film": col[1].contents[0],
                         "Year": col[2].contents[0]}
            temp_df = pd.DataFrame(data_dict, index=[0])
            my_df = pd.concat([my_df,temp_df], ignore_index=True)
            count+=1
    else:
        break

# LƯU DATA ĐÃ SCRAP ĐƯỢC VỀ DATABASE SQLITE ===============================================================
# Dùng pandas để chuyể Dataframe my_df thành file .csv và lưu vào csv_path đã khai báo trên đầu script
my_df.to_csv(csv_path)

# Dùng sqlite3 để kết nối với database SQLite đã khai báo trên đầu script
conn = sqlite3.connect(db_name)

# Chuyển toàn bộ DataFrame my_df vào bảng có tên table_name trong SQLite Database đang được kết nối qua conn
my_df.to_sql(table_name, conn, if_exists='replace', index=False)

# Hoàn tất, ngắt kết nối với SQLite Database
conn.close()