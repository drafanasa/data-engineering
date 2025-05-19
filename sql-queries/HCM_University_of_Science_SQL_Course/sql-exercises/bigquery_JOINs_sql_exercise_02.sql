-- Truy vấn: Liệt kê các trưởng phòng gồm mã trưởng phòng, tên trưởng phòng, tên phòng, thành phố và lương
-- Phân tích luồng:
  -- JOIN 2 table employees -e và departments -d theo e.EMPLOYEE_ID = d.MANAGER_ID
  -- JOIN tiếp nối với table location -l theo l.LOCATION_ID = d.LOCATION_ID
  -- Truy vấn các cột d.MANAGER_ID, e.FIRST_NAME, e.LAST_NAME, d.DEPARTMENT_NAME, l.STREET_ADDRESS, l.CITY, l.STATE_PROVINCE, l.COUNTRY_ID và e.SALARY

WITH
cleaned_departments_sql AS (
  SELECT MANAGER_ID, DEPARTMENT_NAME, LOCATION_ID
  FROM `esoteric-ripple-450311-e0.my_dataset.departments`
  WHERE 
    MANAGER_ID IS NOT NULL
    AND LOCATION_ID IS NOT NULL
),

cleaned_employees_sql AS (
  SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME, SALARY
  FROM `esoteric-ripple-450311-e0.my_dataset.employees`
  WHERE
    EMPLOYEE_ID IS NOT NULL
),

cleaned_locations_sql AS (
  SELECT LOCATION_ID, STREET_ADDRESS, CITY, STATE_PROVINCE, COUNTRY_ID
  FROM `esoteric-ripple-450311-e0.my_dataset.locations`
  WHERE LOCATION_ID IS NOT NULL
)

SELECT 
  d.MANAGER_ID AS Manager_ID, 
  e.FIRST_NAME AS First_Name, 
  e.LAST_NAME AS Last_Name, 
  e.SALARY AS Salary,
  d.DEPARTMENT_NAME AS Department,
  CONCAT(
    IFNULL(l.STREET_ADDRESS, 'N/a'), ', ',
    IFNULL(l.CITY, 'N/a'), ', ',
    IFNULL(l.STATE_PROVINCE, 'N/a'), ', ',
    IFNULL(l.COUNTRY_ID, 'N/a')
  ) AS Department_Location

FROM cleaned_departments_sql d
JOIN cleaned_employees_sql e ON e.EMPLOYEE_ID = d.MANAGER_ID
JOIN cleaned_locations_sql l ON l.LOCATION_ID = d.LOCATION_ID

ORDER BY Salary DESC;
