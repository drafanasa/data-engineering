'''
Run the following commands in the terminal. 
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/INSTRUCTOR.csv

python3.11 -m pip install pandas
'''
#==========================================================================
# THƯ VIỆN, SQLITE3 DATABASE VÀ TABLE
#==========================================================================
# Khai báo thư viện
import pandas as pd 
import sqlite3

# Khởi tạo SQLite Database(nếu chưa có)
conn = sqlite3.connect('STAFF.db')  

# Khai báo thuộc tính của table
table_name = 'INSTRUCTOR'
attribute_list = ['ID', 'FNAME', 'LNAME', 'CITY', 'CCODE']

#==========================================================================
# ĐỌC DATASET *.CSV - TẢI RECORDS VÀO SQL TABLE 
#==========================================================================

# Dùng function pd.read_csv() của pandas đọc file .csv -> lưu records vào một Dataframe 'temp_df'
file_path = '/home/project/Access_DB_using_Python_Script/INSTRUCTOR.csv'
temp_df = pd.read_csv(file_path, names = attribute_list)

# Dùng function dataframe.to_sql() của pandas để tải records trong Dataframe 'temp_df' vào SQL Table
temp_df.to_sql(table_name, conn, if_exists = 'replace', index =False)
print('Table is ready')

#==========================================================================
# CHẠY TRUY VẤN QUERY TRÊN DỮ LIỆU 
#==========================================================================

# Truy vấn: Hiện toàn bộ records trong table (lần đầu)
query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

# Truy vấn: Đếm tổng số dòng dữ liệu trong table
query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

# Truy vấn: Thêm vào table 1 dòng dữ liệu với các thông tin sau 
data_dict = {'ID' : [100],
            'FNAME' : ['John'],
            'LNAME' : ['Doe'],
            'CITY' : ['Paris'],
            'CCODE' : ['FR']}
data_append = pd.DataFrame(data_dict)

data_append.to_sql(table_name, conn, if_exists = 'append', index =False)
print('Data appended successfully')

# Truy vấn: Hiện toàn bộ records trong table (lần thứ hai - sau khi append thêm dữ liệu mới)
query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

conn.close() # Đóng kết nối với Database