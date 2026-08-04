# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "1a4c11fc-a852-4237-97e0-a85e41fdad99",
# META       "default_lakehouse_name": "lh_f1_lake_silver",
# META       "default_lakehouse_workspace_id": "576651d3-647c-4541-ad9f-38e5a52d18b0",
# META       "known_lakehouses": [
# META         {
# META           "id": "1a4c11fc-a852-4237-97e0-a85e41fdad99"
# META         }
# META       ]
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# CELL ********************

query = """

WITH year_driver_points AS(

SELECT Year
     , DriverId
     , SUM(Points) AS TotalPoints
  FROM lh_f1_lake_silver.dbo.f1_results
 GROUP
    BY Year
     , DriverId
),

rn_year_driver AS(

SELECT ROW_NUMBER() OVER (PARTITION BY Year ORDER BY TotalPoints DESC) AS RankDriver
     , *
  FROM year_driver_points
)

SELECT Year
     , DriverId
     , TotalPoints
     , RankDriver
  FROM rn_year_driver
 WHERE RankDriver = 1

"""

df = spark.sql(query)

(df.write
   .format('delta')
   .mode('overwrite')
   .saveAsTable('lh_f1_lake_silver.dbo.f1_champions'))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
