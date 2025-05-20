import glob
import pandas as pd 
import xml.etree.ElementTree as ET
from datetime import datetime 

'''Run the following commands in the terminal shell:
a. Download the zip file containing the required data in multiple formats.
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/datasource.zip 

b. Unzip the downloaded file.
unzip datasource.zip

c. Create python file.
touch etl_practice.py
'''

# Chỉ định danh tính cho 2 file "log_file.txt" và "transformed_data.csv"
log_file = "log_file.txt" 
target_file = "transformed_data.csv" 

# EXTRACT ====================================================
# Function đọc dataset .csv (dùng pandas)
def extract_from_csv(file_to_process): 
    # Kiểm soát lỗi (Error Handling) - nếu 1 file bị lỗi thì quy trình vẫn chạy tiếp được
    try:
        dataframe_csv = pd.read_csv(file_to_process) 
        return dataframe_csv
    except Exception as e:
        log_progress(f"Error reading CSV file {file_to_process}: {str(e)}")
        return pd.DataFrame()
        # Giải thích vì sao reture pd.DataFrame():
        #1. Tránh vỡ pipeline
        # Nếu 1 file bị lỗi (ví dụ: hỏng cấu trúc, thiếu cột...), thay vì dừng hẳn ETL thì Function sẽ trả về DataFrame rỗng → chương trình vẫn tiếp tục chạy các file khác.
        #2. Dễ kiểm soát logic nối dữ liệu
        # Trong các Function extract(), có bước kiểm tra .empty hoặc .isna().all() để chủ động loại bỏ DataFrame rỗng.
        #3. Giao diện thống nhất
        # Các Function extract_from_*() luôn trả về một DataFrame — dù thành công hay thất bại — giúp phần còn lại của pipeline không cần phân biệt kiểu trả về, giảm bug.

# Function đọc dataset .json (dùng pandas)
def extract_from_json(file_to_process): 
    # Kiểm soát lỗi (Error Handling) - nếu 1 file bị lỗi thì quy trình vẫn chạy tiếp được
    try:
        dataframe_json = pd.read_json(file_to_process, lines=True) 
        return dataframe_json 
    except Exception as e:
        log_progress(f"Error reading JSON file {file_to_process}: {str(e)}")
        return pd.DataFrame()

# Function đọc dataset .xml (dùng ElementTree)
def extract_from_xml(file_to_process): 
    # Kiểm soát lỗi (Error Handling) - nếu 1 file bị lỗi thì quy trình vẫn chạy tiếp được
    try:
        # Tạo df rỗng với 4 cột là  'car_model', 'year_of_manufacture', 'price', 'fuel'
        dataframe_xml = pd.DataFrame(columns=[ 'car_model', 'year_of_manufacture', 'price', 'fuel']) 
        # Dùng ElementTree để đọc dataset .xml
        tree = ET.parse(file_to_process) 
        root = tree.getroot()
        # Tạo một list trống để chứa các df hợp lệ -> concat luôn một lần (để tránh FutureWarning Pandas)
        list_of_valid_dataframe_1 = [] 
        # Vòng lặp lấy lần lượt từng cụm data  'car_model', 'year_of_manufacture', 'price', 'fuel' trong file .xml
        for person in root: 
            car_model = person.find('car_model').text 
            year_of_manufacture = person.find('year_of_manufacture').text
            price = float(person.find('price').text) 
            fuel = person.find('fuel').text
            # Gán data vừa lấy vào dataframe_xml tạo sẵn
            # Dùng pd.concat thay vì append đã lỗi thời, pd.concat mang lại hiệu quả và 
            # tính linh hoạt tốt hơn, đặc biệt là khi kết hợp nhiều DataFrame
            temp_df = pd.DataFrame([{'car_model':car_model, 'year_of_manufacture':year_of_manufacture, 'price':price, 'fuel':fuel}])
            # Bổ sung: lọc trước khi nối (concat) để bỏ qua các DataFrame rỗng hoặc toàn NaN
            if isinstance(temp_df, pd.DataFrame) and not temp_df.empty and not temp_df.isna().all().all():
                list_of_valid_dataframe_1.append(temp_df)
                
        # Concat 1 lần duy nhất tất cả temp_df hợp lệ đã được lưu vào danh sách list_of_valid_dataframe_1 (để tránh FutureWarning Pandas)
        if list_of_valid_dataframe_1:
            dataframe_xml = pd.concat(list_of_valid_dataframe_1, ignore_index=True) # luôn reset index sau khi concat xong để tránh index bị lặp
        
        return dataframe_xml
    except Exception as e:
        log_progress(f"Error reading XML file {file_to_process}: {str(e)}")
        return pd.DataFrame()

# Function tự động xác định kiểu tệp dataset (.csv, .json hay .xml) rồi call function đọc dataset tương ứng
def extract(): 
    # Tạo df rỗng với 4 cột là 'car_model', 'year_of_manufacture', 'price', 'fuel'
    extracted_data = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel']) 

    # Tạo một list trống để chứa các df hợp lệ -> concat luôn một lần (để tránh FutureWarning Pandas)
    list_of_valid_dataframe_2 = []
     
    # Dùng thư viện glob để nhận diện tất cả dataset .csv 
    # (ngoại trừ target_file = "transformed_data.csv")
    for csvfile in glob.glob("*.csv"): 
        if csvfile != target_file: 
            temp_df = pd.DataFrame(extract_from_csv(csvfile))
            # Lọc trước khi nối (concat) để bỏ qua các DataFrame rỗng hoặc toàn NaN
            if isinstance(temp_df, pd.DataFrame) and not temp_df.empty and not temp_df.isna().all().all():
                list_of_valid_dataframe_2.append(temp_df)
         
    # tương tự cho dataset .json
    for jsonfile in glob.glob("*.json"): 
        temp_df = pd.DataFrame(extract_from_json(jsonfile))
        # Lọc trước khi nối (concat) để bỏ qua các DataFrame rỗng hoặc toàn NaN
        if isinstance(temp_df, pd.DataFrame) and not temp_df.empty and not temp_df.isna().all().all():
            list_of_valid_dataframe_2.append(temp_df) 
     
    # tương tự cho dataset .xml
    for xmlfile in glob.glob("*.xml"): 
        temp_df = pd.DataFrame(extract_from_xml(xmlfile))
        # Lọc trước khi nối (concat) để bỏ qua các DataFrame rỗng hoặc toàn NaN
        if isinstance(temp_df, pd.DataFrame) and not temp_df.empty and not temp_df.isna().all().all():
            list_of_valid_dataframe_2.append(temp_df)

    # Concat 1 lần duy nhất tất cả df hợp lệ đã được lưu vào danh sách list_of_valid_dataframe_2 (để tránh FutureWarning Pandas)
    if list_of_valid_dataframe_2:
        extracted_data = pd.concat(list_of_valid_dataframe_2, ignore_index=True)

    # trả về df chứa dữ liệu thô được tổng hợp từ các dataset thập cẩm    
    return extracted_data 

# TRANSFORMATION ==============================================
# Fucntion chuyển đổi đơn vị đo dữ liệu theo yêu cầu bài toán
def transform(data): 
    # Chuyển car_model sang Capitalize Case
    data['car_model'] = data['car_model'].astype(str).str.title()
    # Làm tròn price thành 2 số thập phân
    data['price'] = round(data.price,2) 
    # Chuyển đổi year_of_manufacture sang int
    #data['year_of_manufacture'] = pd.to_numeric(data['year_of_manufacture'], errors='coerce')
    # Chuyển đổi year_of_manufacture sang datetime (nếu chỉ có năm → gán mặc định là 1/1/<năm>)
    data['year_of_manufacture'] = pd.to_datetime(
        data['year_of_manufacture'], 
        format='%Y',  # định dạng năm
        errors='coerce'  # nếu lỗi thì trả về NaT
    )
    # Trả về data đã được chuyển đổi
    return data 

# Ghi chú: có thể bổ sung các function khác để data cleaning, validation,... trong bước này

# LOADING VÀ LOGGING===========================================
# Function chuyển df được lưu trong df transformed_data thành file .csv có bí danh 'target_file' để lưu trữ
def load_data(target_file, transformed_data): 
    transformed_data.to_csv(target_file, index=False) # Tham số index=False giúp tránh ghi chỉ số (index) không cần thiết vào file CSV.

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