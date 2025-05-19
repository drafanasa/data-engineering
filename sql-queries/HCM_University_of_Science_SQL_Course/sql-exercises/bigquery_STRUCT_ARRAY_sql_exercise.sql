-- Truy vấn 1: Tạo bảng pets_and_toys theo yêu cầu
/*
CREATE OR REPLACE TABLE `esoteric-ripple-450311-e0.my_dataset.pets_and_toys` AS
SELECT
  1 AS ID,
  'Moon' AS Name,
  9 AS Age,
  'Dog' AS Animal,
  STRUCT('McFly' AS Name, 'Frisbee' AS Type) AS Toy
UNION ALL
SELECT
  2, 'Ripley', 7, 'Cat',
  STRUCT('FluFly', 'Feather')
UNION ALL
SELECT
  3, 'Napoleon', 1, 'Fish',
  STRUCT('Eddy', 'Castle');
*/

-- Truy vấn 2: Hiển thị bảng vừa tạo 
/*
SELECT
  Name AS Pet_Name,
  Toy.Name AS Toy_Name,
  Toy.Type AS Toy_Type
FROM `esoteric-ripple-450311-e0.my_dataset.pets_and_toys`
ORDER By Name;
*/

-- Truy vấn 3: Tạo bảng pets_and_toys_type theo yêu cầu
/*
CREATE OR REPLACE TABLE `esoteric-ripple-450311-e0.my_dataset.pets_and_toys_type` AS
SELECT
  'Moon' AS Name, 9 AS Age, 'Dog' AS Animal, ['Frisbee','Bone', 'Rope'] AS Toys
UNION ALL
SELECT
  'Napoleon', 1, 'Fish', ['Ball','Castle']
UNION ALL
SELECT
  'Ripley', 7, 'Cat', ['Feather','Ball'];
*/

-- Truy vấn 4: Làm phẳng mảng với UNNEST() hoặc CROSS JOIN... AS...
/*
-- Tạo CTE từ table pets_and_toys_type
WITH pets_and_toys_type_sql AS(
  SELECT Name, Toys
  FROM `esoteric-ripple-450311-e0.my_dataset.pets_and_toys_type`
)

-- Làm phẳng mảng với CROSS JOIN... AS... --
SELECT Name, flattened_Toys  
FROM pets_and_toys_type,  
CROSS JOIN pets_and_toys_type.Toys AS flattened_Toys;

-- Cú pháp UNNEST() tương đương --
SELECT Name, flattened_Toys 
FROM pets_and_toys_type,  
UNNEST(Toys) AS flattened_Toys;
*/

-- Truy vấn 5: Tạo bảng more_pets_and_toys theo yêu cầu
/*
CREATE OR REPLACE TABLE `esoteric-ripple-450311-e0.my_dataset.more_pets_and_toys` AS
SELECT
 1 AS ID,
 'Moon' AS Name,
 9 AS Age,
 'Dog' AS Animal,
 [STRUCT(
  ['MCFly','Scully','Pusheen'] AS Name,
  ['Frisbee','Bone', 'Rope'] AS Type
)] AS Toys
UNION ALL
SELECT
  2,'Ripley', 7, 'Cat', 
  [STRUCT(
    ['Fluffy','Robert'],
    ['Feather','Ball']
  )]
UNION ALL
SELECT
  3, 'Napoleon', 1, 'Fish', 
  [STRUCT(
    ['Eddy'],
    ['Castle']
  )];
*/

-- Truy vấn 6: Hiển thị bảng vừa tạo 
SELECT
  p.Name AS Pet_Name,
  toy_name,
  toy_type
FROM `esoteric-ripple-450311-e0.my_dataset.more_pets_and_toys` AS p,
UNNEST(p.Toys) AS t
JOIN UNNEST(t.Name) AS toy_name WITH OFFSET AS idx_name
JOIN UNNEST(t.Type) AS toy_type WITH OFFSET AS idx_type
ON idx_name = idx_type
