-- Truy vấn: Cho biết có bao nhiêu dòng trong table?
/*
SELECT COUNT(*) AS count_row
FROM `bigquery-public-data.usa_names.usa_1910_current`;
*/

-- Truy vấn: Thống kê đếm số dòng năm (không tính NULL), tính từ năm 2017
/*
SELECT COUNT(year) AS count_row_year_after2017
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year >= 2017;
*/

-- Truy vấn: Kiểm tra xem có tên em bé nào bị thiếu không? Cho biết có bao nhiêu tên em bé không bị trùng?
/*
SELECT 
  COUNT(*) - COUNT(name) AS count_null_name,
  COUNT(DISTINCT name) AS count_distinct_name
FROM `bigquery-public-data.usa_names.usa_1910_current`;
*/

-- Truy vấn: Thống kê có bao nhiêu tên em bé theo năm và theo nam/nữ, tính từ năm 2017. Cho nhận xét?
/*
SELECT 
  year,
  gender,
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year >= 2017
GROUP BY year, gender
ORDER BY year;
*/
/*
Nhận xét:
-  Tổng số em bé được đặt tên vẫn cao, tuy nhiên có thể có xu hướng giảm nhẹ trong một số năm gần đây (đặc biệt sau 2020 — giai đoạn dịch COVID-19).
- Sự chênh lệch giữa bé trai và bé gái không quá lớn, tuy nhiên bé trai thường nhiều hơn một chút về tổng số.
- Biểu đồ theo năm có thể cho thấy xu hướng đặt tên hiện đại tăng lên hoặc sự sụt giảm dân số sinh sản.
*/

-- Truy vấn: Thống kê có bao nhiêu tên em bé theo năm và theo nam/nữ, tính từ năm 2017
/*
SELECT 
  year,
  COUNT(DISTINCT CASE WHEN gender = 'F' THEN name END) AS count_female_name,
  COUNT(DISTINCT CASE WHEN gender = 'M' THEN name END) AS count_male_name
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year >= 2017
GROUP BY year
ORDER BY year;
*/

-- Truy vấn: Trong năm 2021, cho biết 5 tiểu bang có nhiều tên em bé được đặt nhất (không tính trùng tên)
/*
SELECT 
  state,
  year,
  COUNT(name) AS total_name
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year = 2021
GROUP BY state, year
ORDER BY total_name DESC
LIMIT 5;
*/

-- Truy vấn: Liệt kê trong năm 2021 ở tiểu bang California 5 tên em bé nam và 5 tên em bé nữ được đặt tên nhiều nhất
/*
SELECT 
  state,
  year,
  COUNT(name) AS total_name
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year = 2021
GROUP BY state, year
ORDER BY total_name DESC
LIMIT 5;
*/

-- Truy vấn: Liệt kê trong năm 2021 ở tiểu bang California (CA) 5 tên em bé nam và 5 tên em bé nữ được đặt tên nhiều nhất
/*
WITH ranked_names AS (
  SELECT 
    name,
    gender,
    SUM(number) AS total_number,
    -- Note: dùng WINDOW FUNCTION + FILTER BY ROW_NUMBER() để đảm bảo mỗi giới chỉ lấy 5 tên phổ biến nhất
    ROW_NUMBER() OVER ( -- Gán số thứ tự tăng dần trong nhóm (không trùng)
      PARTITION BY gender -- nhóm theo (giống GROUP BY)
      ORDER BY SUM(number) DESC -- xếp thứ tự trong nhóm
    ) AS rank
    
  FROM `bigquery-public-data.usa_names.usa_1910_current`
  WHERE year = 2021 AND state = 'CA'
  GROUP BY name, gender
)

SELECT name, gender, total_number
FROM ranked_names
WHERE rank <= 5
ORDER BY gender, total_number DESC;
*/

-- Truy vấn: Liệt kê 10 tên chung (unisex) được đặt cho cả bé trai và bé gái, có tổng lượt đặt tên cao nhất trong năm 2021
-- Phân tích luồng:
  --Lọc dữ liệu năm 2021
  --Gom nhóm theo name, đếm COUNT(DISTINCT gender) để biết tên nào xuất hiện cho cả hai giới
  --Tính tổng số bé được đặt tên đó (SUM(number))
  --Lọc ra tên có đủ cả hai giới (COUNT(DISTINCT gender) = 2)
  --Sắp xếp theo total_number DESC, lấy top 10

SELECT 
  name,
  SUM(number) AS total_number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year = 2021
GROUP BY name
HAVING COUNT(DISTINCT gender) = 2
ORDER BY total_number DESC
LIMIT 10;






