-- Truy vấn: Cho biết có bao nhiêu dòng của năm 2021
/*SELECT COUNT(*) AS count_rows
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year = 2021;*/

-- Truy vấn: Cho biết có bao nhiêu dòng của năm 2021 trong tiểu bang CA
/*SELECT COUNT(*) AS count_rows
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year = 2021 AND state = 'CA';*/

-- Truy vấn: Liệt kê 1000 dòng đầu tiên, sắp theo năm giảm dần
/*SELECT *
FROM `bigquery-public-data.usa_names.usa_1910_current`
ORDER BY year DESC
LIMIT 1000;*/

-- Truy vấn: Liệt kê các mã tiểu bang theo thứ tự mã tiểu bang tăng dần. Cho biết có bao nhiêu tiểu bang?
/*WITH state_sql AS (
  SELECT state
  FROM `bigquery-public-data.usa_names.usa_1910_current`
  WHERE state IS NOT NULL
  GROUP BY state
  ORDER BY state
)
SELECT COUNT(*) FROM state_sql;*/

-- Truy vấn: Liệt kê các năm theo thứ tự năm giảm dần. Cho biết năm nhỏ nhất và năm lớn nhất?
-- Liệt kê các năm theo thứ tự năm giảm dần
/*SELECT year
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year DESC;*/

-- Cho biết năm nhỏ nhất và năm lớn nhất
/*SELECT
  MIN(year) AS min_year,
  MAX(year) AS max_year
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year IS NOT NULL;*/

-- Truy vấn: Trong năm 2021 cho biết 10 tên được đặt nhiều nhất của tiểu bang CA. Thử sắp tăng theo tên (nếu được); Thử tính tổng các số lượng (nếu được)
/*SELECT name, number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year=2021 AND state='CA'
ORDER BY number DESC
LIMIT 10;*/

-- Truy vấn: Trong năm 2021 cho biết 10 tên theo giới tính Nam được đặt nhiều nhất của tiểu bang CA
/*SELECT name, gender, number, 
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year=2021 AND gender='M' AND state='CA'
ORDER BY number DESC
LIMIT 10;*/

-- Truy vấn: Trong tiểu bang CA, liệt kê các tên bắt đầu là 'Aad'. Sắp xếp tăng theo năm và giới tính
/*SELECT year, name, gender, number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE state = 'CA' AND name LIKE 'Aad%'
ORDER BY year, gender
LIMIT 100;*/

-- Truy vấn: Trong tiểu bang CA năm 2021, cho biết các tên có số lượng đặt nhỏ hơn hay bằng 55. Sắp giảm theo số lượng và chỉ lấy 1000 dòng đầu tiên (số lượng đặt trung bình xấp xỉ 55.40)
/*SELECT name, number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE state = 'CA' AND year=2021 AND number <= 55
ORDER BY number DESC
LIMIT 1000;*/

-- Truy vấn: Trong tiểu bang CA năm 2021, đếm các tên có số lượng đặt lớn hơn 55
/*SELECT COUNT(*) AS count_name -- COUNT(*) sẽ đếm tất cả các dòng khớp điều kiện, không cần kiểm tra null như COUNT(name)
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE state = 'CA' AND year=2021 AND number > 55;*/

-- Truy vấn: Trong tiểu bang CA năm 2021, cho biết các tên có số lượng đặt lớn nhất và nhỏ nhất
WITH 
name_sql AS (
  SELECT name, number
  FROM `bigquery-public-data.usa_names.usa_1910_current`
  WHERE state = 'CA' AND year = 2021
),

number_stats_sql AS (
  SELECT
    MIN(number) AS min_used_name,
    MAX(number) AS max_used_name
  FROM name_sql
)

SELECT name, number
FROM name_sql
WHERE number = (SELECT min_used_name FROM number_stats_sql)
   OR number = (SELECT max_used_name FROM number_stats_sql)
ORDER BY number DESC;
