import glob
import pandas as pd 
import xml.etree.ElementTree as ET
from datetime import datetime 

'''Run the following commands in the terminal shell:
a. Download the zip file containing the required data in multiple formats.
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IB

b. Unzip the downloaded file.
unzip source.zip

c. Create python file.
touch etl_code.py
'''

# Chỉ định danh tính cho 2 file "log_file.txt" và "transformed_data.csv"
log_file = "log_file.txt" 
target_file = "transformed_data.csv" 

# EXTRACT ====================================================
# Function đọc dataset .csv (dùng pandas)
def extract_from_csv(file_to_process): 
    dataframe_csv = pd.read_csv(file_to_process) 
    return dataframe_csv

# Function đọc dataset .json (dùng pandas)
def extract_from_json(file_to_process): 
    dataframe_json = pd.read_json(file_to_process, lines=True) 
    return dataframe_json 

# Function đọc dataset .xml (dùng ElementTree)
def extract_from_xml(file_to_process): 
    # Tạo df rỗng với 3 cột là "name", "height", "weight"
    dataframe_xml = pd.DataFrame(columns=["name", "height", "weight"]) 
    # Dùng ElementTree để đọc dataset .xml
    tree = ET.parse(file_to_process) 
    root = tree.getroot() 
    # Vòng lặp lấy lần lượt từng cụm data "name", "height", "weight" trong file .xml
    for person in root: 
        name = person.find("name").text 
        height = float(person.find("height").text) 
        weight = float(person.find("weight").text) 
        # Gán data vừa lấy vào dataframe_xml tạo sẵn
        # Dùng pd.concat thay vì append đã lỗi thời, pd.concat mang lại hiệu quả và 
        # tính linh hoạt tốt hơn, đặc biệt là khi kết hợp nhiều DataFrame
        dataframe_xml = pd.concat([
            dataframe_xml, 
            pd.DataFrame([
                {"name":name, "height":height, "weight":weight}
            ])
        ], ignore_index=True) # luôn reset index sau khi concat xong để tránh index bị lặp
    return dataframe_xml

# Function tự động xác định kiểu tệp dataset (.csv, .json hay .xml) rồi call function đọc dataset tương ứng
def extract(): 
    # Tạo df rỗng với 3 cột là "name", "height", "weight"
    extracted_data = pd.DataFrame(columns=['name','height','weight']) 
     
    # Dùng thư viện glob để nhận diện tất cả dataset .csv 
    # (ngoại trừ target_file = "transformed_data.csv")
    for csvfile in glob.glob("*.csv"): 
        if csvfile != target_file: 
            extracted_data = pd.concat([
                extracted_data, 
                pd.DataFrame(extract_from_csv(csvfile)) # Call function extract_from_csv
                ], ignore_index=True)
         
    # tương tự cho dataset .json
    for jsonfile in glob.glob("*.json"): 
        extracted_data = pd.concat([
            extracted_data, 
            pd.DataFrame(extract_from_json(jsonfile)) # Call function extract_from_json
            ], ignore_index=True) 
     
    # tương tự cho dataset .xml
    for xmlfile in glob.glob("*.xml"): 
        extracted_data = pd.concat([
            extracted_data, 
            pd.DataFrame(extract_from_xml(xmlfile)) # Call function extract_from_xml
            ], ignore_index=True) 

    # trả về df chứa dữ liệu thô được tổng hợp từ các dataset thập cẩm    
    return extracted_data 

# TRANSFORMATION ==============================================
# Fucntion chuyển đổi đơn vị đo dữ liệu theo yêu cầu bài toán
def transform(data): 
    # Chuyển inchs thành meters và làm tròn 2 số thập phân, biết 1 inch = 0.0254 meters
    data['height'] = round(data.height * 0.0254,2) 
 
    # Chuyển pounds thành kilograms và làm tròn 2 số thập phân, biết 1 pound = 0.45359237 kilograms
    data['weight'] = round(data.weight * 0.45359237,2) 
    
    # Trả về data đã được chuyển đổi
    return data 

# Ghi chú: có thể bổ sung các function khác để data cleaning, validation,... trong bước này

# LOADING VÀ LOGGING===========================================
# Function chuyển df được lưu trong df transformed_data thành file .csv có bí danh 'target_file' để lưu trữ
def load_data(target_file, transformed_data): 
    transformed_data.to_csv(target_file) 

# Fucntion ghi lại lịch sử hoạt động của pipeline này thành file .txt có bí danh 'log_file' để lưu trữ
def log_progress(message): 
    timestamp_format = '%Y-%m-%d %H:%M:%S'  # chuẩn ISO, dễ đọc và xử lý
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 

# CHẠY ETL VÀ GHI NHẬN LOG ====================================
# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
 
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract() 
 
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
 
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
 
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
 
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_data(target_file,transformed_data) 
 
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
 
# Log the completion of the ETL process 
log_progress("ETL Job Ended") 