-- Thực hiện query: truy vấn 100 dòng đầu
/*SELECT *
FROM bigquery-public-data.census_bureau_usa.population_by_zip_2010 
LIMIT 100;*/

-- Thực hiện query: đếm số dòng của dataset
/*SELECT COUNT(*) AS row_count 
FROM bigquery-public-data.census_bureau_usa.population_by_zip_2010;*/

-- Thực hiện query: in ra population min, max, avg
/*SELECT 
  MIN(population) AS min_population,
  MAX(population) AS max_population,
  AVG(population) AS avg_population,
FROM bigquery-public-data.census_bureau_usa.population_by_zip_2010
WHERE population > 0;*/

-- Thực hiện query: giống câu trên nhưng có dùng thêm định dạng hiển thị FORMAT
/*SELECT 
  MIN(population) AS min_pop, 
  FORMAT("%'d",MAX(population)) AS max_pop, 
  FORMAT("%.2f", AVG(population)) AS avg_pop
FROM bigquery-public-data.census_bureau_usa.population_by_zip_2010
WHERE population > 0;*/

-- Thực hiện query: lọc các dòng có zipcode là 602 và gender là male
/*SELECT geo_id,population
FROM bigquery-public-data.census_bureau_usa.population_by_zip_2010
WHERE zipcode = '602' AND gender = 'male';*/

-- Thực hiện query: lọc các dòng có zipcode là 602 và thống kê đếm theo gender
SELECT gender, COUNT(*) AS count_rows
FROM bigquery-public-data.census_bureau_usa.population_by_zip_2010
WHERE zipcode = '602' AND gender IS NOT NULL
GROUP BY gender;
