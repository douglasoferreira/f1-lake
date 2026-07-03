CREATE OR ALTER VIEW [dbo].[f1_champions] AS

WITH year_driver_points AS(

SELECT Year
     , DriverId
     , SUM(Points) AS TotalPoints
  FROM [lh_f1_lake_bronze].[dbo].[f1_results]
 GROUP
    BY Year
     , DriverId
),

rn_year_driver AS(

SELECT ROW_NUMBER() OVER (PARTITION BY Year ORDER BY TotalPoints DESC) AS rank_driver
     , *
  FROM year_driver_points
)

SELECT Year
     , DriverId
     , TotalPoints
  FROM rn_year_driver
 WHERE rank_driver = 1;