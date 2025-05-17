-- Truy vấn: Liệt kê các station của 10 lượt thuê xe có thời gian thuê cao nhất (duration_minutes) với thời gian bắt đầu (start_time) của năm 2022. Sắp giảm theo số trạm xe (number_of_dock)
/*
SELECT station_id, name, number_of_docks
FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations`
WHERE 
  -- Nếu subquery trả về nhiều dòng (10 dòng), nên dùng IN thay vì dùng toán tử "=" để tránh lỗi Scalar subquery produced more than one element
  station_id IN (
    SELECT start_station_id
    FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` 
    WHERE
    -- Lọc thời gian bắt đầu (start_time) của năm 2022
      DATE(start_time) BETWEEN '2022-01-01' AND '2022-12-31'
    -- Lọc 10 lượt thuê xe có thời gian thuê cao nhất (duration_minutes)
    ORDER BY duration_minutes DESC
    LIMIT 10
  )
  AND name IS NOT NULL
  AND number_of_docks IS NOT NULL
  AND number_of_docks > 0
ORDER BY number_of_docks DESC;
*/
------------------------------------------------------------------------------------
-- Truy vấn: Liệt kê các station mà trong năm 2013 (tính theo start_time) không có lượt thuê xe nào. Sắp tăng theo tên station (name)
-- Phân tích luồng: lấy những station_id có sẵn trong bảng bikeshare_stations nhưng không có trong bảng bikeshare_trips năm 2013
/*
SELECT 
  station_id, 
  name
FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations`
WHERE 
  station_id NOT IN (
    SELECT DISTINCT start_station_id
    FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` 
    WHERE DATE(start_time) BETWEEN '2013-01-01' AND '2013-12-31'
      AND start_station_id IS NOT NULL
  )
ORDER BY name;
*/
------------------------------------------------------------------------------------
-- Truy vấn: Liệt kê các lượt thuê xe trong năm 2022 của những station có nhiều số trạm xe nhất. Sắp tăng theo start_station_id, sắp giảm theo duration_minutes. Chọn 1000 dòng
-- Phân tích luồng:
-- Lọc các station_id có nhiều trạm xe nhất (number_of_docks), xếp giảm dần và không trùng, không null.
-- Lọc các trip_id trong năm 2022, có start_station_id thuộc các station_id có nhiều trạm xe nhất
-- Sắp tăng theo start_station_id, sắp giảm theo duration_minutes. Chọn 1000 dòng
/*
SELECT trip_id, start_station_id
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` 
WHERE 
  DATE(start_time) BETWEEN '2022-01-01' AND '2022-12-31'
  AND start_station_id IN (
    SELECT station_id
    FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations`
    WHERE number_of_docks IS NOT NULL AND number_of_docks > 0
    ORDER BY number_of_docks DESC
  )
ORDER BY
  start_station_id ASC,
  duration_minutes DESC
LIMIT 1000;
*/

-- Truy vấn: Liệt kê các station có lượt thuê xe trong năm 2022 của bikeid 920 với 10 lượt thuê có duration_minutes cao nhất. Sắp tăng theo tên station
-- Phân tích đề:
-- Bảng bikeshare_trips: 
  -- Lọc các start_station_id và trip_id với điều kiện: năm 2022 và bikeid là 920
  -- Xếp theo thứ tự duration_minutes giảm dần, chọn 10 giá trị đầu tiên
-- Bảng bikeshare_stations:
  -- Lọc name và trip_id theo station_id match với start_station_id
  -- Xếp theo thứ tự name tăng dần A-Z
/*
WITH
bikeid920_2022_sql AS (
  SELECT start_station_id, trip_id
  FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` 
  WHERE 
    DATE(start_time) BETWEEN '2022-01-01' AND '2022-12-31'
    AND bike_id = '920'
  ORDER BY duration_minutes DESC
  LIMIT 10
)
SELECT 
  t.trip_id,
  s.station_id,
  s.name AS station_name
FROM bikeid920_2022_sql t --t là bí danh cho bảng bikeid920_2022_sql (CTE)
JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` s --s là bí danh cho bảng bikeshare_stations
  ON t.start_station_id = s.station_id
WHERE s.name IS NOT NULL
ORDER BY station_name ASC;
*/

-- Truy vấn: Trong năm 2022 cho biết các lượt thuê xe có duration_minutes nhỏ hơn 4 của các station có địa chỉ (address) chứa chuỗi “Red River”
-- Phân tích luồng:
  -- bikeshare_trips: Lọc trip_id theo điều kiện: năm 2022 AND duration_minutes < 4 AND 
  -- JOIN bảng bikeshare_trips với bikeshare_strations theo station_id để lọc địa chỉ address LIKE '%Red River%'

WITH
short_trips_2022_sql AS (
  SELECT trip_id, start_station_id
  FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
  WHERE
    DATE(start_time) BETWEEN '2022-01-01' AND '2022-12-31'
    AND duration_minutes < 4
    AND duration_minutes > 0
    AND duration_minutes IS NOT NULL
)
SELECT 
  t.trip_id,
  s.station_id,
  s.name AS station_name,
  s.address AS station_adress
FROM short_trips_2022_sql t --t là bí danh cho bảng short_trips_2022_sql (CTE)
JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` s --s là bí danh cho bảng bikeshare_stations
  ON t.start_station_id = s.station_id
WHERE 
  s.name IS NOT NULL
  AND s.address LIKE '%Red River%'
ORDER BY s.name;







