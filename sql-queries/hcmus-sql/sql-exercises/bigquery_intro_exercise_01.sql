-- Query: Xem DS 100 dòng đầu
-- SELECT *
-- FROM esoteric-ripple-450311-e0.my_dataset.athletes
-- LIMIT 100;
------------------------------
-- Query: Xem thông tin tất cả VĐV nữ
-- SELECT id, name, nationality, date_of_birth, height, weight, sport
-- FROM esoteric-ripple-450311-e0.my_dataset.athletes
-- WHERE sex = 'female'
-- LIMIT 100;
------------------------------
-- Query: Xem thông tin tất cả VĐV nữ + xếp thứ tự order theo tên
-- SELECT id, name, nationality, date_of_birth, height, weight, sport
-- FROM esoteric-ripple-450311-e0.my_dataset.athletes
-- WHERE sex = 'female'
-- ORDER BY name
-- LIMIT 100;
------------------------------
-- Query: Xem thông tin tất cả VĐV: ĐK1 'giới tính nữ' + ĐK2 'không có huy chương'
-- SELECT id, name, nationality, date_of_birth, height, weight, sport, total
-- FROM esoteric-ripple-450311-e0.my_dataset.athletes
-- WHERE sex = 'female' AND total = 0
-- ORDER BY name
-- LIMIT 100;
------------------------------
-- Query: Đếm tổng số dòng có trong dataset
-- SELECT COUNT(*) AS count_row
-- FROM esoteric-ripple-450311-e0.my_dataset.athletes;
------------------------------
-- Query: Thống kê min, max, avg của các cột age, height, weight (ĐK = giới tính nữ)
/*SELECT 
  MIN(age) AS min_age, 
  MAX(age) AS max_age, 
  AVG(age) AS avg_age, 
  MIN(height) AS min_height, 
  MAX(height) AS max_height,
  AVG(height) AS avg_height, 
  MIN(weight) AS min_weight, 
  MAX(weight) AS max_weight,
  AVG(weight) AS avg_weight
FROM esoteric-ripple-450311-e0.my_dataset.athletes
WHERE sex = 'female';*/
------------------------------
-- Query: Thống kê thống kê count, min, max, avg theo nam/nữ riêng biệt
/*SELECT sex, 
  COUNT(*) AS count_, 
  MIN(age) AS min_age, 
  MAX(age) AS max_age, 
  AVG(age) AS avg_age, 
  AVG(height) AS avg_height, 
  AVG(weight) AS avg_weight
FROM esoteric-ripple-450311-e0.my_dataset.athletes
GROUP BY sex;*/
------------------------------
-- Query: Thống kê min, max, avg theo nam/nữ là các vận động viên có huy chương
/*SELECT sex, 
  COUNT(*) AS count_, 
  MIN(age) AS min_age, 
  MAX(age) AS max_age, 
  AVG(age) AS avg_age, 
  AVG(height) AS avg_height, 
  AVG(weight) AS avg_weight
FROM esoteric-ripple-450311-e0.my_dataset.athletes
WHERE total > 0
GROUP BY sex;*/
------------------------------
-- Query: cho biết 10 vận động viên có nhiều huy chương nhất (TOP 10)
/*SELECT id, name, total 
FROM esoteric-ripple-450311-e0.my_dataset.athletes
WHERE total > 0
ORDER BY total DESC
LIMIT 10;*/
------------------------------
-- Query: cho biết 10 vận động viên nữ có nhiều huy chương nhất
/*SELECT id, name, sex, total 
FROM esoteric-ripple-450311-e0.my_dataset.athletes
WHERE sex = "female" AND total > 0
ORDER BY total DESC
LIMIT 10;*/
------------------------------
-- Query: cho biết 10 vận động viên nữ có nhiều huy chương vàng nhất
SELECT id, name, sex, gold
FROM esoteric-ripple-450311-e0.my_dataset.athletes
WHERE sex = "female" AND gold > 0
ORDER BY gold DESC
LIMIT 10;