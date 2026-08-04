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

import mlflow
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from synapse.ml.lightgbm import LightGBMClassifier

df = spark.read.table('abt_champions')

# SEMMA

#### 1. SAMPLE

df = df.withColumn('Year', F.split(F.col('DateRef'), '-')[0].cast('int'))
df_year_round = df.select('Year', 'DateRef').drop_duplicates()

window = Window.orderBy('DateRef').partitionBy('Year')
df_year_round = df_year_round.withColumn('RowNumber', F.row_number().over(window))

df = df.join(df_year_round, on=['Year', 'DateRef'])

df_oot = df.filter(F.col('Year') == 2025)
df_analytics = df.filter(F.col('Year') < 2025)

ignored_columns = ['RowNumber', 'DateRef', 'Year', 'DriverId', 'RankDriver']
features = [col for col in df_analytics.columns if col not in ignored_columns]

train_years, tests_years = df_analytics.select('Year').drop_duplicates().randomSplit([0.8, 0.2], seed=42)

df_train = df_analytics.join(train_years, 'Year')
df_test = df_analytics.join(tests_years, 'Year')

#### 2. EXPLORE
isna = df_train.select([F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in features])
isna = isna.unpivot([], features, 'Feature', 'QtyNull').filter(F.col('QtyNull') > 0)

### 3. MODIFY
assembler = VectorAssembler(
    inputCols=features,
    outputCol='features_vector'
)

model = LightGBMClassifier(
    featuresCol='features_vector',
    labelCol='RankDriver',
    objective='binary',
    isUnbalance=True
)

pipeline = Pipeline(stages=[assembler, model])

mlflow.set_experiment(experiment_name="ex_f1_driver_champion")

### 4. MODEL
with mlflow.start_run():

### 5. ASSESS
    model_trained = pipeline.fit(df_train)
    predict_train = model_trained.transform(df_train)
    predict_test = model_trained.transform(df_test)
    predict_oot = model_trained.transform(df_oot)

    evaluator = BinaryClassificationEvaluator(
        labelCol='RankDriver',
        rawPredictionCol='probability',
        metricName='areaUnderROC'
    )

    auc_train = evaluator.evaluate(predict_train)
    auc_test = evaluator.evaluate(predict_test)
    auc_oot = evaluator.evaluate(predict_oot)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
