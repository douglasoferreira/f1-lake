# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "460593bc-4ec8-4022-a245-6267e6795edc",
# META       "default_lakehouse_name": "lh_f1_lake_gold",
# META       "default_lakehouse_workspace_id": "576651d3-647c-4541-ad9f-38e5a52d18b0",
# META       "known_lakehouses": [
# META         {
# META           "id": "1a4c11fc-a852-4237-97e0-a85e41fdad99"
# META         },
# META         {
# META           "id": "460593bc-4ec8-4022-a245-6267e6795edc"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

query = """

SELECT A.* 
     , COALESCE(B.RankDriver, 0) AS RankDriver
  FROM fs_f1_driver_all A
  LEFT
  JOIN lh_f1_lake_silver.dbo.f1_champions     B ON A.DriverId = B.DriverId
                                          AND YEAR(A.DateRef) = B.Year
 WHERE A.DateRef BETWEEN '2000-01-01' AND '2025-12-31'
 ORDER
    BY A.DateRef DESC

"""

df = spark.sql(query)

(df.write
   .format('delta')
   .mode('overwrite')
   .saveAsTable('lh_f1_lake_gold.dbo.abt_champions'))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
