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

-- 1. Determine all unique reference dates
WITH tb_dates AS(
SELECT DISTINCT CAST(Date AS DATE) AS DateRef
     , Year                        AS YearRef
  FROM lh_f1_lake_silver.dbo.f1_results
),

--2. Cross-reference: For every reference date, find all sessions that happened before it
past_sessions AS(
SELECT A.DateRef
     , A.YearRef
     , B.*
  FROM tb_dates   A
  JOIN lh_f1_lake_silver.dbo.f1_results B ON B.Date < A.DateRef
),

-- 3. Filter for eligible drivers (active in the reference year or (reference year - 2))
drivers_selected AS(
SELECT DISTINCT
       DateRef
     , DriverId
  FROM past_sessions
 WHERE YearRef - Year <= 2
),

-- 4. Get distinct rounds that occurred before each reference date
distinct_rounds AS(
SELECT DISTINCT
       DateRef
     , Year
     , RoundNumber
  FROM past_sessions
),

-- 5. Rank those rounds chronologically backwards for each reference date
ranked_rounds AS(
SELECT DateRef
     , Year
     , RoundNumber
     , ROW_NUMBER() OVER(PARTITION BY DateRef ORDER BY Year DESC, RoundNumber DESC) AS RowNum
 FROM distinct_rounds
),

-- 7. Keep only the last 10 rounds per reference date
last_rounds AS(
SELECT DateRef
     , Year
     , RoundNumber
  FROM ranked_rounds
 WHERE RowNum <= {last_rounds}
),

-- 8. Bring it all together: Join past sessions with our eligible drivers and our 10 race filter
tb_results AS(
SELECT A.*
  FROM past_sessions    A
  JOIN drivers_selected B ON A.DateRef     = B.DateRef
                         AND A.DriverId    = B.DriverId
  JOIN last_rounds      C ON A.DateRef     = C.DateRef
                         AND A.Year        = C.Year
                         AND A.RoundNumber = C.RoundNumber
),

-- 9. Perform the final aggregation grouped by the reference date and driver
tb_stats AS(
SELECT DateRef
     , DriverId 
     , COUNT(DISTINCT Year)                                                                                              AS QtdSeasons
     , COUNT(*)                                                                                                          AS QtdSessions
     , SUM(CASE WHEN Status = 'Finished'     OR Status LIKE '+%'                           THEN 1            ELSE 0 END) AS QtdSessFinished
     , SUM(CASE WHEN                             Mode = 'Race'                             THEN 1            ELSE 0 END) AS QtdRace
     , SUM(CASE WHEN Mode = 'Race'           AND (Status = 'Finished' OR Status LIKE '+%') THEN 1            ELSE 0 END) AS QtdSessFinRace
     , SUM(CASE WHEN                             Mode = 'Sprint'                           THEN 1            ELSE 0 END) AS QtdSprint
     , SUM(CASE WHEN Mode = 'Sprint'         AND (Status = 'Finished' OR Status LIKE '+%') THEN 1            ELSE 0 END) AS QtdSessFinSprint
     , SUM(CASE WHEN Position  = 1                                                         THEN 1            ELSE 0 END) AS Qtd1Pos
     , SUM(CASE WHEN Position  = 1           AND Mode = 'Race'                             THEN 1            ELSE 0 END) AS Qtd1PosRace
     , SUM(CASE WHEN Position  = 1           AND Mode = 'Sprint'                           THEN 1            ELSE 0 END) AS Qtd1PosSprint
     , SUM(CASE WHEN Position <= 3                                                         THEN 1            ELSE 0 END) AS QtdPodio
     , SUM(CASE WHEN Position <= 3           AND Mode = 'Race'                             THEN 1            ELSE 0 END) AS QtdPodioRace
     , SUM(CASE WHEN Position <= 3           AND Mode = 'Sprint'                           THEN 1            ELSE 0 END) AS QtdPodioSprint
     , COALESCE(SUM(Points)                                                                                         , 0) AS QtdPoints
     , SUM(CASE WHEN                             Mode = 'Race'                             THEN Points       ELSE 0 END) AS QtdPointsRace
     , SUM(CASE WHEN                             Mode = 'Sprint'                           THEN Points       ELSE 0 END) AS QtdPointsSprint
     , COALESCE(AVG(GridPosition)                                                                                   , 0) AS AvgGridPos
     , COALESCE(AVG(CASE WHEN                    Mode = 'Race'                             THEN GridPosition    END), 0) AS AvgGridPosRace
     , COALESCE(AVG(CASE WHEN                    Mode = 'Sprint'                           THEN GridPosition    END), 0) AS AvgGridPosSprint
     , COALESCE(AVG(Position)                                                                                       , 0) AS AvgPos
     , COALESCE(AVG(CASE WHEN                    Mode = 'Race'                             THEN Position        END), 0) AS AvgPosRace
     , COALESCE(AVG(CASE WHEN                    Mode = 'Sprint'                           THEN Position        END), 0) AS AvgPosSprint
     , SUM(CASE WHEN GridPosition = 1                                                      THEN 1            ELSE 0 END) AS Qtd1GridPos
     , SUM(CASE WHEN GridPosition = 1        AND Mode = 'Race'                             THEN 1            ELSE 0 END) AS Qtd1GridPosRace
     , SUM(CASE WHEN GridPosition = 1        AND Mode = 'Sprint'                           THEN 1            ELSE 0 END) AS Qtd1GridPosSprint
     , SUM(CASE WHEN GridPosition = 1        AND Position = 1                              THEN 1            ELSE 0 END) AS Qtd1PoleWin
     , SUM(CASE WHEN GridPosition = 1        AND Position = 1 AND Mode = 'Race'            THEN 1            ELSE 0 END) AS Qtd1PoleWinRace
     , SUM(CASE WHEN GridPosition = 1        AND Position = 1 AND Mode = 'Sprint'          THEN 1            ELSE 0 END) AS Qtd1PoleWinSprint
     , SUM(CASE WHEN Points > 0                                                            THEN 1            ELSE 0 END) AS QtdSessPoints
     , SUM(CASE WHEN Points > 0              AND Mode = 'Race'                             THEN 1            ELSE 0 END) AS QtdSessPointsRace
     , SUM(CASE WHEN Points > 0              AND Mode = 'Sprint'                           THEN 1            ELSE 0 END) AS QtdSessPointsSprint
     , SUM(CASE WHEN Position < GridPosition                                               THEN 1            ELSE 0 END) AS QtdSessOvertake
     , SUM(CASE WHEN Position < GridPosition AND Mode = 'Race'                             THEN 1            ELSE 0 END) AS QtdSessOvertakeRace
     , SUM(CASE WHEN Position < GridPosition AND Mode = 'Sprint'                           THEN 1            ELSE 0 END) AS QtdSessOvertakeSprint
     , COALESCE(AVG(GridPosition - Position)                                                                        , 0) AS AvgOvertake
     , COALESCE(AVG(CASE WHEN Mode = 'Race'                                        THEN GridPosition - Position END), 0) AS AvgOvertakeRace
     , COALESCE(AVG(CASE WHEN Mode = 'Sprint'                                      THEN GridPosition - Position END), 0) AS AvgOvertakeSprint
     , SUM(CASE WHEN Position <= 5                                                         THEN 1            ELSE 0 END) AS Qtd5Pos
     , SUM(CASE WHEN Position <= 5           AND Mode = 'Race'                             THEN 1            ELSE 0 END) AS Qtd5PosRace
     , SUM(CASE WHEN Position <= 5           AND Mode = 'Sprint'                           THEN 1            ELSE 0 END) AS Qtd5PosSprint
     , SUM(CASE WHEN GridPosition <= 5                                                     THEN 1            ELSE 0 END) AS Qtd5GridPos
     , SUM(CASE WHEN GridPosition <= 5       AND Mode = 'Race'                             THEN 1            ELSE 0 END) AS Qtd5GridPosRace
     , SUM(CASE WHEN GridPosition <= 5       AND Mode = 'Sprint'                           THEN 1            ELSE 0 END) AS Qtd5GridPosSprint
  FROM tb_results  
 GROUP  
    BY DateRef, DriverId
)

SELECT *
  FROM tb_stats
 ORDER
    BY DriverId, DateRef DESC

"""

last_rounds = 20

df = spark.sql(query.format(last_rounds = last_rounds))

(df.write
   .format('delta')
   .mode('overwrite')
   .saveAsTable(f'lh_f1_lake_gold.dbo.fs_f1_driver_last_{last_rounds}'))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
