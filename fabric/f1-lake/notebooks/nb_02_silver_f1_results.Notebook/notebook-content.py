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
# META         },
# META         {
# META           "id": "1a4c11fc-a852-4237-97e0-a85e41fdad99"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import pyspark.sql.functions as F
from delta.tables import DeltaTable

# 1. Table Path Configuration
table_bronze_source = 'lh_f1_lake_bronze.dbo.f1_results'
table_bronze_target = 'lh_f1_lake_silver.dbo.f1_results'

# 2. Read data from the Bronze Layer
df = spark.read.table(table_bronze_source)

# 3. Data Type and Time Scale Transformations (Data Cleansing Layer)
latest_ingestion = df.select(F.max('IngestionDate')).first()[0]

# Micro-batch Isolation (Filter by the latest ingestion to optimize CPU/Memory)
if latest_ingestion:
    df_isolated = df.filter(F.col('IngestionDate') == latest_ingestion)
else:
    df_isolated = df

df_results = (df_isolated

    # Integer Types (Business Rule: there are no fractional positions, laps, or dates)
    .withColumn('Position', F.col('Position').cast('integer'))
    .withColumn('GridPosition', F.col('GridPosition').cast('integer'))
    
    # Time Scaling: Convert raw Microseconds to Decimal Seconds (Optimized for ML/Analytics)
    .withColumn('Q1', (F.col('Q1') / 1E6).cast('double'))
    .withColumn('Q2', (F.col('Q2') / 1E6).cast('double'))
    .withColumn('Q3', (F.col('Q3') / 1E6).cast('double'))
    .withColumn('Time', (F.col('Time') / 1E6).cast('double'))
    
    # More Integer Types for consistency
    .withColumn('Laps', F.col('Laps').cast('integer'))
    .withColumn('Year', F.col('Year').cast('integer'))
    
    # Date: Adjust scale from nanoseconds to seconds and convert to readable Timestamp
    .withColumn('Date', (F.col('Date') / 1E9).cast('timestamp'))
    .withColumn('RoundNumber', F.col('RoundNumber').cast('integer'))

)

# 4. Check if the Target Silver Table already exists in the catalog
table_exists = spark.catalog.tableExists(table_bronze_target)

if not table_exists:
    # If the table does not exist, create it for the first time
    df_results.write.format('delta').mode('overwrite').saveAsTable(table_bronze_target)

else:
    # If the table exists, execute a MERGE (Upsert) to avoid duplicates
    delta_target = DeltaTable.forName(spark, table_bronze_target)

    (delta_target.alias('target')
        .merge(
            source = df_results.alias('source'),
            condition = '''
                target.Year = source.Year
                AND target.RoundNumber = source.RoundNumber
                AND target.Mode = source.Mode
                AND target.DriverId = source.DriverId
            '''
        )
        # Data Quality Guard: If data matches, update it with the latest corrected version
        .whenMatchedUpdateAll()
        # If the data does not exist, insert it as a new record
        .whenNotMatchedInsertAll()
        .execute())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
