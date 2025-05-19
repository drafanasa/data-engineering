-- Truy vấn: Chỉ xét dữ liệu trong năm 2022
/*SELECT
unique_key, taxi_id, 
EXTRACT (MONTH FROM trip_start_timestamp) AS trip_month,
trip_seconds, trip_miles, fare, tips, tolls, extras, trip_total, payment_type, company
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
WHERE trip_start_timestamp BETWEEN '2022-01-01' AND '2022-12-31'; --Lọc trực tiếp trên cột thời gian gốc (trip_start_timestamp) giúp BigQuery tận dụng partition pruning nếu bảng đã được phân vùng theo cột này + Giảm lượng dữ liệu đọc, từ đó tăng tốc độ truy vấn và giảm chi phí xử lý.*/

-- Truy vấn: Tiếp tục từ truy vấn trên, liệt kê 1000 dòng đầu tiên, sắp theo trip_total giảm dần. Hướng dẫn: dùng CTE
/*WITH 
trip_2022_sql AS (
  SELECT
  unique_key, taxi_id, 
  EXTRACT (MONTH FROM trip_start_timestamp) AS trip_month,
  trip_seconds, trip_miles, fare, tips, tolls, extras, trip_total, payment_type, company
  FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
  WHERE trip_start_timestamp BETWEEN '2022-01-01' AND '2022-12-31'
)
SELECT *
FROM trip_2022_sql
ORDER BY trip_total DESC
LIMIT 1000;*/

-- Truy vấn: Cho biết trip_2022_sql có bao nhiêu dòng dữ liệu?
/*WITH 
trip_2022_sql AS (
  SELECT
  unique_key, taxi_id, 
  EXTRACT (MONTH FROM trip_start_timestamp) AS trip_month,
  trip_seconds, trip_miles, fare, tips, tolls, extras, trip_total, payment_type, company
  FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
  WHERE trip_start_timestamp BETWEEN '2022-01-01' AND '2022-12-31'
)
SELECT COUNT(*) AS count_rows
FROM trip_2022_sql;*/

-- Truy vấn: Liệt kê các công ty theo thứ tự tăng của TÊN công ty. Có bao nhiêu công ty?
-- Liệt kê các công ty theo thứ tự tăng của TÊN công ty
/*SELECT DISTINCT company
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
WHERE
  company IS NOT NULL
  AND trip_start_timestamp BETWEEN '2022-01-01' AND '2022-12-31'
ORDER BY company;
-- Có bao nhiêu công ty?
SELECT COUNT(DISTINCT company) AS total_companies
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
WHERE
  company IS NOT NULL
  AND trip_start_timestamp BETWEEN '2022-01-01' AND '2022-12-31';*/

-- Truy vấn:	Liệt kê các loại thanh toán theo thứ tự tăng của loại thanh toán. Có bao nhiêu loại thanh toán?
-- Liệt kê các loại thanh toán theo thứ tự tăng của loại thanh toán
/*SELECT DISTINCT payment_type
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
WHERE
  payment_type IS NOT NULL
  AND trip_start_timestamp BETWEEN '2022-01-01' AND '2022-12-31'
ORDER BY payment_type;
-- Có bao nhiêu loại thanh toán?
SELECT COUNT(DISTINCT payment_type) AS total_payment_type
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
WHERE
  payment_type IS NOT NULL
  AND trip_start_timestamp BETWEEN '2022-01-01' AND '2022-12-31';*/

-- Truy vấn:	Liệt kê 10 chuyến xe có thời gian đi (tính theo phút) nhiều nhất (làm tròn 2 số lẻ)
/*WITH 
trip_2022_sql AS (
  SELECT
  unique_key, taxi_id, trip_seconds, trip_miles, fare, tips, tolls, extras, trip_total, payment_type, company,
  EXTRACT (MONTH FROM trip_start_timestamp) AS trip_month
  FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
  WHERE trip_start_timestamp BETWEEN '2022-01-01' AND '2022-12-31'
)
SELECT ROUND(trip_seconds / 60.0, 2) AS trip_minutes,
FROM trip_2022_sql
ORDER BY trip_minutes DESC
LIMIT 10;*/


-- Truy vấn: Cho biết hãng xe nào có số tiền khách trả ít nhất
/*WITH 
trip_2022_sql AS (
  SELECT
    company, trip_total -- Tối ưu query: Chỉ chọn cột cần thiết trong CTE để giảm dữ liệu phải quét
  FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
  WHERE 
    DATE(trip_start_timestamp) BETWEEN '2022-01-01' AND '2022-12-31' -- Tối ưu query: Nếu bảng được partition theo ngày, dùng DATE(trip_start_timestamp) thay vì BETWEEN (với dataset rất lớn)
    AND trip_total IS NOT NULL
    AND trip_total > 0
    AND company IS NOT NULL -- Tối ưu query: Lọc dữ liệu càng sớm càng tốt (Early Filtering), tránh data rác tốn tài nguyên
)

SELECT 
  company,
  SUM(trip_total) AS company_rev
FROM trip_2022_sql
GROUP BY company
ORDER BY company_rev ASC -- Tối ưu query: Không ORDER BY các cột không cần thiết
LIMIT 10;*/

-- Truy vấn: Liệt kê 10 hãng xe trong tháng 12 có số tiền khách trả nhiều nhất
/*WITH 
trip_dec_2022_sql AS (
  SELECT
    company, trip_total -- Tối ưu query: Chỉ chọn cột cần thiết trong CTE để giảm dữ liệu phải quét
  FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
  WHERE 
    DATE(trip_start_timestamp) BETWEEN '2022-12-01' AND '2022-12-31' -- Tối ưu query: Nếu bảng được partition theo ngày, dùng DATE(trip_start_timestamp) thay vì BETWEEN (với dataset rất lớn)
    AND trip_total IS NOT NULL
    AND trip_total > 0
    AND company IS NOT NULL -- Tối ưu query: Lọc dữ liệu càng sớm càng tốt (Early Filtering), tránh data rác tốn tài nguyên
)

SELECT 
  company,
  SUM(trip_total) AS company_rev
FROM trip_dec_2022_sql
GROUP BY company
ORDER BY company_rev DESC -- Tối ưu query: Không ORDER BY các cột không cần thiết
LIMIT 10;*/

-- Truy vấn: Cho biết tổng số tiền khách trả cho tất cả chuyến xe của mọi hãng xe trong tháng 12 
SELECT 
  ROUND(SUM(trip_total), 2) AS total_revenue_dec_2022
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE 
  DATE(trip_start_timestamp) BETWEEN '2022-12-01' AND '2022-12-31'
  AND trip_total > 0;















