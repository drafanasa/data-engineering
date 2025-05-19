'''
Run the following commands in the terminal. 
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/Departments.csv

python3.11 -m pip install pandas
'''
#==========================================================================
# THƯ VIỆN, SQLITE3 DATABASE VÀ TABLE
#==========================================================================
import pandas as pd 
import sqlite3

conn = sqlite3.connect('STAFF.db')  

table_name = 'Departments'
attribute_list = ['DEPT_ID', 'DEP_NAME', 'MANAGER_ID', 'LOC_ID']

#==========================================================================
# ĐỌC DATASET *.CSV - TẢI RECORDS VÀO SQL TABLE 
#==========================================================================

# Dùng function pd.read_csv() của pandas đọc file .csv -> lưu records vào một Dataframe 'temp_df'
file_path = '/home/project/Access_DB_using_Python_Script/Departments.csv'
temp_df = pd.read_csv(file_path, names = attribute_list)

# Dùng function dataframe.to_sql() của pandas để tải records trong Dataframe 'temp_df' vào SQL Table
temp_df.to_sql(table_name, conn, if_exists = 'replace', index =False)
print('Table is ready')

# Thêm vào table 1 dòng dữ liệu với các thông tin sau 
data_dict = {'DEPT_ID' : [9],
            'DEP_NAME' : ['Quality Assurance'],
            'MANAGER_ID' : ['30010'],
            'LOC_ID' : ['L0010']}
data_append = pd.DataFrame(data_dict)

data_append.to_sql(table_name, conn, if_exists = 'append', index =False)

#==========================================================================
# CHẠY TRUY VẤN QUERY TRÊN DỮ LIỆU 
#==========================================================================
# Truy vấn 1: View all entries
query_statement = f'SELECT * FROM {table_name}'
query_ouput = pd.read_sql(query_statement, conn)
print('\n Truy vấn 1: View all entries')
print(query_statement)
print(query_ouput)

# Truy vấn 2: View only the department names
query_statement = f'SELECT DEP_NAME FROM {table_name}'
query_output = pd.read_sql(query_statement, conn)
print('\n Truy vấn 2: View only the department names')
print(query_statement)
print(query_output)

# Truy vấn 3: Count the total entries
query_statement = f'SELECT COUNT(*) FROM {table_name}'
query_output = pd.read_sql(query_statement, conn)
print('\n Truy vấn 3: Count the total entries')
print(query_statement)
print(query_output)

conn.close() # Đóng kết nối với Database

