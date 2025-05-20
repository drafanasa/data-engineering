#=========================================================
# CẤU TRÚC CODE CHO MỘT ETL THU THẬP DỮ LIỆU GPD CÁC NƯỚC
#=========================================================

#=========================================================
# CÀI ĐẶT CÁC THƯ VIỆN PYTHON CẦN THIẾT
#=========================================================
import numpy as np 
import pandas as pd 
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from io import StringIO

#=========================================================
# KHAI BÁO CÁC THỰC THỂ
#=========================================================
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
csv_name = 'Countries_by_GDP.csv'
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
table_attribs = ["Country", "Region", "GDP_USD_millions"]
log_file = "logfile.txt"       # log thông thường
log_error_file = "log_error.txt"  # log riêng lỗi (nếu muốn)

#==============================================
# EXTRACT - THU THẬP DỮ LIỆU TỪ WEBSITE
#==============================================
def extract(url, table_attribs):
    # Tải HTML của trang web cần scrap data bằng thư viện Request + BeautifulSoup 
    html_page = requests.get(url).text

    # Dùng thư viện phân tích HTML 'lxml' để thay cho phương pháp cũ là 'html_parse'
    soup = BeautifulSoup(html_page, 'lxml') 

    # Dùng hàm pandas.read_html() của pandas để tự động trích xuất các DataFrames sạch từ HTML
    # Gói chuỗi HTML bằng StringIO để tuân thủ chuẩn mới của pandas, tránh FutureWarning
    tables = pd.read_html(StringIO(str(soup)), na_values=["—", "N/A"]) 
     
    # Check thủ công trên web HTML: bảng GDP cần lấy là table thứ 3 (index = 2)
    gdp_table = tables[2]  

    # Làm phẳng tên cột nếu là MultiIndex (khi HTML có cột gộp span)
    if isinstance(gdp_table.columns[0], tuple):
        gdp_table.columns = [' | '.join(col).strip() for col in gdp_table.columns]
    else:
        gdp_table.columns = [col.strip() for col in gdp_table.columns]

    
    # Lọc chỉ các cột cần thiết (theo tên đã làm phẳng)
    col_selected_list = [
        'Country/Territory | Country/Territory',
        'UN region | UN region',
         'IMF[1][13] | Estimate'
         ]
    gdp_table_col_selected = gdp_table[col_selected_list]

    # Đổi tên cột theo table_attribs đã khai báo
    gdp_table_col_selected.columns = table_attribs
    
    # Tạo df là dataframe hoàn chỉnh (kết quả bước EXTRACT) dựa trên gdp_table
    df = gdp_table_col_selected
    return df


# KIỂM TRA KẾT QUẢ BƯỚC EXTRACT
'''
df_extracted = extract(url, table_attribs)
print(df_extracted.head(50))
print(df_extracted.info())
'''

#=================================================
# TRANFORM - CHUẨN HOÁ VÀ LÀM SẠCH DỮ LIỆU
#=================================================
def transform(df):

    # Case này không cần bỏ dấu "," vì hàm .read_html() của pandas đã tự xử lý
    # df['GDP_USD_millions'] = df['GDP_USD_millions'].str.replace(',', '', regex=False)

    # Ép kiểu từ object -> float
    df['GDP_USD_millions'] = df['GDP_USD_millions'].astype(float)

    # Tạo cột mới 'GDP_USD_billions' - Đổi đơn vị từ million sang billion, làm tròn 2 chữ số
    df['GDP_USD_billions'] = (df['GDP_USD_millions'] / 1000).round(2)

    # Xoá cột cũ 'GDP_USD_millions'
    df = df.drop(columns='GDP_USD_millions')

    return df

# KIỂM TRA KẾT QUẢ BƯỚC TRANFORM
'''
df_extracted = extract(url, table_attribs)
df_tranformed = transform(df_extracted)
print(df_tranformed.head(50))
print(df_tranformed.info())
'''

#=================================================================================
# LOADING - TẢI DỮ LIỆU VÀO DATASET .CSV VÀ SQLITE3 DATABASE .DB
#=================================================================================

def load_to_csv(df, csv_name):
    # Chuyển dataframe thành file .CSV đã khai báo (nếu chưa có sẽ tự động khởi tạo file .CSV)
    df.to_csv(csv_name, index=False)

def load_to_db(df, db_name, table_name):
    # Dùng function .to_sql() của pandas để tải records trong dataframe vào SQL Table
    # Tham số chunksize=1000 để tránh lỗi bộ nhớ với dữ liệu lớn
    df.to_sql(table_name, conn, if_exists = 'replace', index =False, chunksize=1000)

# KIỂM TRA KẾT QUẢ BƯỚC LOAD
'''
df_extracted = extract(url, table_attribs)
df_tranformed = transform(df_extracted)
df_to_csv = load_to_csv(df_tranformed, csv_name)
df_to_db = load_to_db(df_tranformed, db_name, table_name)
'''

#==============================================================
# QUERYING - TRUY CẬP VÀO DATABASE ĐỂ TRUY VẤN DỮ LIỆU
#==============================================================

def run_query(query_statement, db_name):
    # Thực hiện truy vấn và đọc vào DataFrame
    df = pd.read_sql(query_statement, conn)

    # In truy vấn và kết quả
    print(query_statement)
    print(df)

# KIỂM TRA KẾT QUẢ BƯỚC QUERYING
'''
df_extracted = extract(url, table_attribs)
df_tranformed = transform(df_extracted)
df_to_csv = load_to_csv(df_tranformed, csv_name)
df_to_db = load_to_db(df_tranformed, db_name, table_name)
query_statement = f"""
SELECT * 
FROM {table_name}
WHERE 
    Country != 'World'
    AND Region IN('Asia', 'Europe')
    AND GDP_USD_billions IS NOT NULL
    AND GDP_USD_billions >= 500
ORDER BY Region, GDP_USD_billions DESC
LIMIT 50;
"""
my_query = run_query(query_statement, db_name)
'''

#=================================================================================
# LOGGING - GHI NHẬN LỊCH SỬ THỰC THI VÀ ERROR (NẾU CÓ)
#=================================================================================

def log_progress(message, error=False):
    timestamp_format = '%Y-%m-%d %H:%M:%S' # Format chuẩn ISO
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    
    log_entry = f"{timestamp}, {'ERROR' if error else 'INFO'}, {message}\n"
    
    try:
        with open(log_file, "a") as f:
            f.write(log_entry)
        # Nếu là lỗi, ghi thêm vào log lỗi riêng
        if error:
            with open(log_error_file, "a") as f_err:
                f_err.write(log_entry)
    except Exception as e:
        # Nếu không thể ghi log, in lỗi ra console (không đệ quy log)
        print(f"[Logging thất bại] {timestamp} | {str(e)}")


''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''
#=================================================================================
# FUNCTION CALL - GỌI PIPELINE ETL VÀ QUERY DỮ LIỆU
#=================================================================================
# Declaring known values
log_progress('Preliminaries complete. Initiating ETL process.')

# Call extract() function
df_extracted = extract(url, table_attribs)
log_progress('Data extraction complete. Initiating Transformation process.')

# Call transform() function
df_tranformed = transform(df_extracted)
log_progress('Data transformation complete. Initiating loading process.')

# Call load_to_csv()
df_to_csv = load_to_csv(df_tranformed, csv_name)
log_progress('Data saved to CSV file.')

# Initiate SQLite3 connection
conn = sqlite3.connect(db_name)
log_progress('SQL Connection initiated.')

# Call load_to_db()
df_to_db = load_to_db(df_tranformed, db_name, table_name)
log_progress('Data loaded to Database as table. Running the query.')

# Call run_query()
query_statement = f"""
SELECT * 
FROM {table_name}
WHERE 
    Country != 'World'
    AND Region IN('Asia', 'Europe')
    AND GDP_USD_billions IS NOT NULL
    AND GDP_USD_billions >= 500
ORDER BY Region, GDP_USD_billions DESC
LIMIT 50;
"""
my_query = run_query(query_statement, db_name)
log_progress('Process Complete.')

# Close SQLite3 connection
conn.close()
log_progress('SQLite3 connection closed.')


