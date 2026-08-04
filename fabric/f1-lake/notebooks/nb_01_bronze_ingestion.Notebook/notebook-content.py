# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "15215b1d-3951-4a29-aded-24ea3c563716",
# META       "default_lakehouse_name": "lh_f1_lake_bronze",
# META       "default_lakehouse_workspace_id": "576651d3-647c-4541-ad9f-38e5a52d18b0",
# META       "known_lakehouses": [
# META         {
# META           "id": "15215b1d-3951-4a29-aded-24ea3c563716"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

# 1. Source Path Configuration (Files)
origin_path = 'abfss://ws_portfolio_fabric@onelake.dfs.fabric.microsoft.com/lh_f1_lake_bronze.Lakehouse/Files/Results'

# 2. Rigid Schema Definition
schema = StructType([
    StructField('DriverNumber', StringType(), True),
    StructField('BroadcastName', StringType(), True),
    StructField('Abbreviation', StringType(), True),
    StructField('DriverId', StringType(), True),
    StructField('TeamName', StringType(), True),
    StructField('TeamColor', StringType(), True),
    StructField('TeamId', StringType(), True),
    StructField('FirstName', StringType(), True),
    StructField('LastName', StringType(), True),
    StructField('FullName', StringType(), True),
    StructField('HeadshotUrl', StringType(), True),
    StructField('CountryCode', StringType(), True),
    StructField('Position', DoubleType(), True),
    StructField('GridPosition', DoubleType(), True),
    StructField('Q1', LongType(), True),
    StructField('Q2', LongType(), True),
    StructField('Q3', LongType(), True),
    StructField('Time', LongType(), True),
    StructField('Status', StringType(), True),
    StructField('Points', DoubleType(), True),
    StructField('Laps', DoubleType(), True),
    StructField('Year', LongType(), True),
    StructField('Date', LongType(), True),
    StructField('Mode', StringType(), True),
    StructField('RoundNumber', LongType(), True),
    StructField('OfficialEventName', StringType(), True),
    StructField('Country', StringType(), True),
    StructField('Location', StringType(), True)
])

# 3. Read raw data as a Stream (Native Parquet Streaming for Fabric)
df_source = (spark.readStream
             .format('parquet')
             .schema(schema)
             .load(origin_path))

# 4. Inject Audit columns (Data Governance)

df_results = (df_source
              .withColumn('FilePath', F.input_file_name())
              .withColumn('IngestionDate', F.current_timestamp()))

# 5. Write Incrementally to Bronze Table (Append-Only)
checkpoint_path = 'abfss://ws_portfolio_fabric@onelake.dfs.fabric.microsoft.com/lh_f1_lake_bronze.Lakehouse/Files/checkpoints/f1_results'

query = (df_results.writeStream
         .format('delta')
         .outputMode('append')
         .option('checkpointLocation', checkpoint_path)
         .toTable('lh_f1_lake_bronze.dbo.f1_results'))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
