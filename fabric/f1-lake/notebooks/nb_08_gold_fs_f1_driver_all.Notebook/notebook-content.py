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
# META           "id": "460593bc-4ec8-4022-a245-6267e6795edc"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

query = """

SELECT A.DateRef
     , A.DriverId
     , A.QtdSeasons AS QtdSeasons_life
     , A.QtdSessions AS QtdSessions_life
     , A.QtdSessFinished AS QtdSessFinished_life
     , A.QtdRace AS QtdRace_life
     , A.QtdSessFinRace AS QtdSessFinRace_life
     , A.QtdSprint AS QtdSprint_life
     , A.QtdSessFinSprint AS QtdSessFinSprint_life
     , A.Qtd1Pos AS Qtd1Pos_life
     , A.Qtd1PosRace AS Qtd1PosRace_life
     , A.Qtd1PosSprint AS Qtd1PosSprint_life
     , A.QtdPodio AS QtdPodio_life
     , A.QtdPodioRace AS QtdPodioRace_life
     , A.QtdPodioSprint AS QtdPodioSprint_life
     , A.QtdPoints AS QtdPoints_life
     , A.QtdPointsRace AS QtdPointsRace_life
     , A.QtdPointsSprint AS QtdPointsSprint_life
     , A.AvgGridPos AS AvgGridPos_life
     , A.AvgGridPosRace AS AvgGridPosRace_life
     , A.AvgGridPosSprint AS AvgGridPosSprint_life
     , A.AvgPos AS AvgPos_life
     , A.AvgPosRace AS AvgPosRace_life
     , A.AvgPosSprint AS AvgPosSprint_life
     , A.Qtd1GridPos AS Qtd1GridPos_life
     , A.Qtd1GridPosRace AS Qtd1GridPosRace_life
     , A.Qtd1GridPosSprint AS Qtd1GridPosSprint_life
     , A.Qtd1PoleWin AS Qtd1PoleWin_life
     , A.Qtd1PoleWinRace AS Qtd1PoleWinRace_life
     , A.Qtd1PoleWinSprint AS Qtd1PoleWinSprint_life
     , A.QtdSessPoints AS QtdSessPoints_life
     , A.QtdSessPointsRace AS QtdSessPointsRace_life
     , A.QtdSessPointsSprint AS QtdSessPointsSprint_life
     , A.QtdSessOvertake AS QtdSessOvertake_life
     , A.QtdSessOvertakeRace AS QtdSessOvertakeRace_life
     , A.QtdSessOvertakeSprint AS QtdSessOvertakeSprint_life
     , A.AvgOvertake AS AvgOvertake_life
     , A.AvgOvertakeRace AS AvgOvertakeRace_life
     , A.AvgOvertakeSprint AS AvgOvertakeSprint_life
     , A.Qtd5Pos AS Qtd5Pos_life
     , A.Qtd5PosRace AS Qtd5PosRace_life
     , A.Qtd5PosSprint AS Qtd5PosSprint_life
     , A.Qtd5GridPos AS Qtd5GridPos_life
     , A.Qtd5GridPosRace AS Qtd5GridPosRace_life
     , A.Qtd5GridPosSprint AS Qtd5GridPosSprint_life
     , B.QtdSeasons AS QtdSeasons_last10
     , B.QtdSessions AS QtdSessions_last10
     , B.QtdSessFinished AS QtdSessFinished_last10
     , B.QtdRace AS QtdRace_last10
     , B.QtdSessFinRace AS QtdSessFinRace_last10
     , B.QtdSprint AS QtdSprint_last10
     , B.QtdSessFinSprint AS QtdSessFinSprint_last10
     , B.Qtd1Pos AS Qtd1Pos_last10
     , B.Qtd1PosRace AS Qtd1PosRace_last10
     , B.Qtd1PosSprint AS Qtd1PosSprint_last10
     , B.QtdPodio AS QtdPodio_last10
     , B.QtdPodioRace AS QtdPodioRace_last10
     , B.QtdPodioSprint AS QtdPodioSprint_last10
     , B.QtdPoints AS QtdPoints_last10
     , B.QtdPointsRace AS QtdPointsRace_last10
     , B.QtdPointsSprint AS QtdPointsSprint_last10
     , B.AvgGridPos AS AvgGridPos_last10
     , B.AvgGridPosRace AS AvgGridPosRace_last10
     , B.AvgGridPosSprint AS AvgGridPosSprint_last10
     , B.AvgPos AS AvgPos_last10
     , B.AvgPosRace AS AvgPosRace_last10
     , B.AvgPosSprint AS AvgPosSprint_last10
     , B.Qtd1GridPos AS Qtd1GridPos_last10
     , B.Qtd1GridPosRace AS Qtd1GridPosRace_last10
     , B.Qtd1GridPosSprint AS Qtd1GridPosSprint_last10
     , B.Qtd1PoleWin AS Qtd1PoleWin_last10
     , B.Qtd1PoleWinRace AS Qtd1PoleWinRace_last10
     , B.Qtd1PoleWinSprint AS Qtd1PoleWinSprint_last10
     , B.QtdSessPoints AS QtdSessPoints_last10
     , B.QtdSessPointsRace AS QtdSessPointsRace_last10
     , B.QtdSessPointsSprint AS QtdSessPointsSprint_last10
     , B.QtdSessOvertake AS QtdSessOvertake_last10
     , B.QtdSessOvertakeRace AS QtdSessOvertakeRace_last10
     , B.QtdSessOvertakeSprint AS QtdSessOvertakeSprint_last10
     , B.AvgOvertake AS AvgOvertake_last10
     , B.AvgOvertakeRace AS AvgOvertakeRace_last10
     , B.AvgOvertakeSprint AS AvgOvertakeSprint_last10
     , B.Qtd5Pos AS Qtd5Pos_last10
     , B.Qtd5PosRace AS Qtd5PosRace_last10
     , B.Qtd5PosSprint AS Qtd5PosSprint_last10
     , B.Qtd5GridPos AS Qtd5GridPos_last10
     , B.Qtd5GridPosRace AS Qtd5GridPosRace_last10
     , B.Qtd5GridPosSprint AS Qtd5GridPosSprint_last10
     , C.QtdSeasons AS QtdSeasons_last20
     , C.QtdSessions AS QtdSessions_last20
     , C.QtdSessFinished AS QtdSessFinished_last20
     , C.QtdRace AS QtdRace_last20
     , C.QtdSessFinRace AS QtdSessFinRace_last20
     , C.QtdSprint AS QtdSprint_last20
     , C.QtdSessFinSprint AS QtdSessFinSprint_last20
     , C.Qtd1Pos AS Qtd1Pos_last20
     , C.Qtd1PosRace AS Qtd1PosRace_last20
     , C.Qtd1PosSprint AS Qtd1PosSprint_last20
     , C.QtdPodio AS QtdPodio_last20
     , C.QtdPodioRace AS QtdPodioRace_last20
     , C.QtdPodioSprint AS QtdPodioSprint_last20
     , C.QtdPoints AS QtdPoints_last20
     , C.QtdPointsRace AS QtdPointsRace_last20
     , C.QtdPointsSprint AS QtdPointsSprint_last20
     , C.AvgGridPos AS AvgGridPos_last20
     , C.AvgGridPosRace AS AvgGridPosRace_last20
     , C.AvgGridPosSprint AS AvgGridPosSprint_last20
     , C.AvgPos AS AvgPos_last20
     , C.AvgPosRace AS AvgPosRace_last20
     , C.AvgPosSprint AS AvgPosSprint_last20
     , C.Qtd1GridPos AS Qtd1GridPos_last20
     , C.Qtd1GridPosRace AS Qtd1GridPosRace_last20
     , C.Qtd1GridPosSprint AS Qtd1GridPosSprint_last20
     , C.Qtd1PoleWin AS Qtd1PoleWin_last20
     , C.Qtd1PoleWinRace AS Qtd1PoleWinRace_last20
     , C.Qtd1PoleWinSprint AS Qtd1PoleWinSprint_last20
     , C.QtdSessPoints AS QtdSessPoints_last20
     , C.QtdSessPointsRace AS QtdSessPointsRace_last20
     , C.QtdSessPointsSprint AS QtdSessPointsSprint_last20
     , C.QtdSessOvertake AS QtdSessOvertake_last20
     , C.QtdSessOvertakeRace AS QtdSessOvertakeRace_last20
     , C.QtdSessOvertakeSprint AS QtdSessOvertakeSprint_last20
     , C.AvgOvertake AS AvgOvertake_last20
     , C.AvgOvertakeRace AS AvgOvertakeRace_last20
     , C.AvgOvertakeSprint AS AvgOvertakeSprint_last20
     , C.Qtd5Pos AS Qtd5Pos_last20
     , C.Qtd5PosRace AS Qtd5PosRace_last20
     , C.Qtd5PosSprint AS Qtd5PosSprint_last20
     , C.Qtd5GridPos AS Qtd5GridPos_last20
     , C.Qtd5GridPosRace AS Qtd5GridPosRace_last20
     , C.Qtd5GridPosSprint AS Qtd5GridPosSprint_last20
     , D.QtdSeasons AS QtdSeasons_last40
     , D.QtdSessions AS QtdSessions_last40
     , D.QtdSessFinished AS QtdSessFinished_last40
     , D.QtdRace AS QtdRace_last40
     , D.QtdSessFinRace AS QtdSessFinRace_last40
     , D.QtdSprint AS QtdSprint_last40
     , D.QtdSessFinSprint AS QtdSessFinSprint_last40
     , D.Qtd1Pos AS Qtd1Pos_last40
     , D.Qtd1PosRace AS Qtd1PosRace_last40
     , D.Qtd1PosSprint AS Qtd1PosSprint_last40
     , D.QtdPodio AS QtdPodio_last40
     , D.QtdPodioRace AS QtdPodioRace_last40
     , D.QtdPodioSprint AS QtdPodioSprint_last40
     , D.QtdPoints AS QtdPoints_last40
     , D.QtdPointsRace AS QtdPointsRace_last40
     , D.QtdPointsSprint AS QtdPointsSprint_last40
     , D.AvgGridPos AS AvgGridPos_last40
     , D.AvgGridPosRace AS AvgGridPosRace_last40
     , D.AvgGridPosSprint AS AvgGridPosSprint_last40
     , D.AvgPos AS AvgPos_last40
     , D.AvgPosRace AS AvgPosRace_last40
     , D.AvgPosSprint AS AvgPosSprint_last40
     , D.Qtd1GridPos AS Qtd1GridPos_last40
     , D.Qtd1GridPosRace AS Qtd1GridPosRace_last40
     , D.Qtd1GridPosSprint AS Qtd1GridPosSprint_last40
     , D.Qtd1PoleWin AS Qtd1PoleWin_last40
     , D.Qtd1PoleWinRace AS Qtd1PoleWinRace_last40
     , D.Qtd1PoleWinSprint AS Qtd1PoleWinSprint_last40
     , D.QtdSessPoints AS QtdSessPoints_last40
     , D.QtdSessPointsRace AS QtdSessPointsRace_last40
     , D.QtdSessPointsSprint AS QtdSessPointsSprint_last40
     , D.QtdSessOvertake AS QtdSessOvertake_last40
     , D.QtdSessOvertakeRace AS QtdSessOvertakeRace_last40
     , D.QtdSessOvertakeSprint AS QtdSessOvertakeSprint_last40
     , D.AvgOvertake AS AvgOvertake_last40
     , D.AvgOvertakeRace AS AvgOvertakeRace_last40
     , D.AvgOvertakeSprint AS AvgOvertakeSprint_last40
     , D.Qtd5Pos AS Qtd5Pos_last40
     , D.Qtd5PosRace AS Qtd5PosRace_last40
     , D.Qtd5PosSprint AS Qtd5PosSprint_last40
     , D.Qtd5GridPos AS Qtd5GridPos_last40
     , D.Qtd5GridPosRace AS Qtd5GridPosRace_last40
     , D.Qtd5GridPosSprint AS Qtd5GridPosSprint_last40
 FROM lh_f1_lake_gold.dbo.fs_f1_driver_life    A
 JOIN lh_f1_lake_gold.dbo.fs_f1_driver_last_10 B ON A.DriverId = B.DriverId
                                                  AND A.DateRef  = B.DateRef
 JOIN lh_f1_lake_gold.dbo.fs_f1_driver_last_20 C ON A.DriverId = C.DriverId
                                                  AND A.DateRef  = C.DateRef
 JOIN lh_f1_lake_gold.dbo.fs_f1_driver_last_40 D ON A.DriverId = D.DriverId
                                                  AND A.DateRef  = D.DateRef
ORDER
   BY A.DateRef, A.DriverId

"""

df = spark.sql(query)

(df.write
   .format('delta')
   .mode('overwrite')
   .saveAsTable('lh_f1_lake_gold.dbo.fs_f1_driver_all'))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
