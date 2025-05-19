-- Truy vấn: Tạo view vwStations là danh sách các station gồm các cột station_id, name, address, number_of_docks
/*
CREATE VIEW `esoteric-ripple-450311-e0.my_dataset.vwStations` AS
SELECT station_id, name, address, number_of_docks
FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations`;

SELECT name
FROM `esoteric-ripple-450311-e0.my_dataset.vwStations`
ORDER BY number_of_docks
LIMIT 10;
*/

-- Truy vấn: 
--Tạo view vwTrips là danh sách các lượt thuê xe gồm các cột trip_id, bikeid, start_time, start_station_id, start_station_name, end_station_id, end_station_name, duration_minutes, start_year, start_month, duration_hours
/*
CREATE VIEW `esoteric-ripple-450311-e0.my_dataset.vwTrips` AS
SELECT 
  trip_id, 
  bike_id, 
  start_time, 
  start_station_id, 
  start_station_name, 
  end_station_id, 
  end_station_name, 
  duration_minutes, 
  EXTRACT (YEAR FROM start_time) AS start_year, 
  EXTRACT (MONTH FROM start_time) AS start_month, 
  ROUND(duration_minutes / 60, 2) AS duration_hours

FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`

WHERE
  trip_id IS NOT NULL
  AND bike_id IS NOT NULL 
  AND start_station_id IS NOT NULL
  AND start_station_name IS NOT NULL
  AND end_station_id IS NOT NULL
  AND end_station_name  IS NOT NULL 
  AND duration_minutes > 0 
  AND duration_minutes IS NOT NULL;
*/
--Từ view vwTrips cho biết các lượt thuê xe trong tháng 12/2022 có duration_hours cao nhất
SELECT *
FROM `esoteric-ripple-450311-e0.my_dataset.vwTrips`
WHERE start_month = 12 AND start_year = 2022
ORDER BY duration_hours DESC
LIMIT 10;
