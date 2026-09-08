# %%
from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from sklearn import ensemble
from sklearn import metrics
from sklearn import model_selection
from sklearn import pipeline

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

mlflow.set_tracking_uri('http://127.0.0.1:5000')
mlflow.set_experiment(experiment_name="ex_f1_lake")

DATA_PATH = Path(__file__).resolve().parent.parent.parent / 'data'

# %%
df = pd.read_csv(DATA_PATH / 'abt_f1_drivers_champion.csv', sep=';')

# %%
# SEMMA

#### 1. SAMPLE

df['Year'] = df['DateRef'].apply(lambda x: x.split('-')[0]).astype(int)

df_year_round = df[['Year', 'DateRef']].drop_duplicates().copy()
df_year_round['RowNumber'] = (df_year_round.sort_values('DateRef', ascending=True)
                                           .groupby('Year')
                                           .cumcount())

df = df.merge(df_year_round, on=['Year', 'DateRef'])

df_oot = df[df['Year'] == 2025].copy()
df_analytics = df[df['Year'] < 2025].copy()

ignored_columns = ['RowNumber', 'DateRef', 'Year', 'DriverId', 'RankDriver']
features = [col for col in df_analytics.columns if col not in ignored_columns]

# %%
gss = model_selection.GroupShuffleSplit(n_splits=1, train_size=0.8, random_state=42)

train_index, test_index = next(
    gss.split(X=df_analytics[features],
              y=df_analytics['RankDriver'],
              groups=df_analytics['Year']
    )
)

df_train = df_analytics.iloc[train_index].copy()
df_test = df_analytics.iloc[test_index].copy()

X_train, y_train = df_train[features], df_train['RankDriver']
X_test, y_test = df_test[features], df_test['RankDriver']
X_oot, y_oot = df_oot[features], df_oot['RankDriver']

# %%
#### 2. EXPLORE
isna = X_train.isna().sum()
isna[isna > 0]

# %%
### 3. MODIFY
clf = ensemble.RandomForestClassifier(
        min_samples_leaf=50, 
        n_estimators=500, 
        random_state=42,
        n_jobs=4)

model = pipeline.Pipeline(steps=[
    ('RandomForest', clf)
])

# %%
### 4. MODEL
with mlflow.start_run():

### 5. ASSESS
    model.fit(X_train, y_train)
    y_train_prob = model.predict_proba(X_train)[:,1]
    auc_train = metrics.roc_auc_score(y_train, y_train_prob)
    roc_train = metrics.roc_curve(y_train, y_train_prob)
    mlflow.log_metric('ROC Train', auc_train)

    y_test_prob = model.predict_proba(X_test)[:,1]
    auc_test = metrics.roc_auc_score(y_test, y_test_prob)
    roc_test = metrics.roc_curve(y_test, y_test_prob)
    mlflow.log_metric('ROC Test', auc_test)

    y_oot_prob = model.predict_proba(X_oot)[:,1]
    auc_oot = metrics.roc_auc_score(y_oot, y_oot_prob)
    roc_oot = metrics.roc_curve(y_oot, y_oot_prob)
    mlflow.log_metric('ROC oot', auc_oot)

    plt.figure(dpi=100)
    plt.plot(roc_train[0], roc_train[1])
    plt.plot(roc_test[0], roc_test[1])
    plt.plot(roc_oot[0], roc_oot[1])
    plt.legend([f'Treino: {auc_train:.4f}', f'Teste: {auc_test:.4f}', f'oot: {auc_oot:.4f}'])
    plt.grid(True)
    plt.title('Curva ROC')
    plt.savefig('roc_curve.png')
    mlflow.log_artifact('roc_curve.png')

    feature_importance = (pd.DataFrame({
        'Feature': X_train.columns,
        'Importance': model.named_steps['RandomForest'].feature_importances_
        })
        .sort_values(by='Importance', ascending=False)
        .reset_index(drop=True)
        .style.format({'Importance': '{:.6%}'}))
    feature_importance.to_html('feature_importances.html')
    mlflow.log_artifact('feature_importances.html')

    model.fit(df_analytics[features], df_analytics['RankDriver'])
    mlflow.sklearn.log_model(sk_model=model, artifact_path='model')