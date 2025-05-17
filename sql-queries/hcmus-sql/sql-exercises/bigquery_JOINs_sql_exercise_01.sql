-- Truy vấn: Liệt kê các vận động viên của thế vận hội 2012. Sắp tăng theo tên vận động viên
/*
SELECT DISTINCT Athlete
FROM `esoteric-ripple-450311-e0.my_dataset.olympics_medals`
WHERE
  Year = 2012
  and Athlete IS NOT NULL
ORDER BY Athlete ASC;
*/
--Truy vấn: Liệt kê 10 vận động viên nữ của thế vận hội 2012 có huy chương vàng. Sắp tăng theo tên vận động viên
/*
SELECT DISTINCT Athlete
FROM `esoteric-ripple-450311-e0.my_dataset.olympics_medals`
WHERE
  Year = 2012
  AND Gender != 'Men'
  AND Athlete IS NOT NULL
ORDER BY Athlete ASC
LIMIT 10;
*/
-- Truy vấn: Trong thế vận hội 2012, liệt kê 10 quốc gia có số huy chương vàng cao nhất (sử dụng JOINs)
-- Phân tích luồng:
  -- Bảng medals: Lọc Year = 2012, Medal = Gold -> Group theo CountryCode + tính TotalGoldMedals -> Trả về CountryCode và TotalGoldMedals
  -- INNER JOIN bảng medals với bảng countries theo CountryCode -> Trả về CountryName + TotalGoldMedals

WITH 
gold_medal_2012_sql AS (
SELECT CountryCode, COUNT(Medal) AS TotalGoldMedal
FROM `esoteric-ripple-450311-e0.my_dataset.olympics_medals`
WHERE
  Year = 2012
  AND Medal = 'Gold'
GROUP BY CountryCode
)

SELECT t2.CountryName, t1.TotalGoldMedal
FROM gold_medal_2012_sql t1
JOIN `esoteric-ripple-450311-e0.my_dataset.olympics_countries` t2 
  ON t1.CountryCode = t2.CountryCode
ORDER BY TotalGoldMedal DESC
LIMIT 10;
