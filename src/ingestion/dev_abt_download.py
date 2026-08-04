# %%
from pathlib import Path

import dotenv
from pyspark.sql import SparkSession
from azure.identity import InteractiveBrowserCredential

# Carrega as variáveis do seu arquivo .env (se houver)
dotenv.load_dotenv()

# 1. Força o VS Code a abrir o navegador no seu PC para você logar com a conta da faculdade
DATA_PATH = Path(__file__).resolve().parent.parent.parent / 'data'
CREDENTIAL = InteractiveBrowserCredential()
token_object = CREDENTIAL.get_token('https://database.windows.net/.default')
access_token = token_object.token

# 2. Inicializa o Spark local com o driver JDBC
spark = SparkSession.builder \
    .appName('Fabric_F1_DataWarehouse_Autenticado') \
    .config('spark.jars.packages', 'com.microsoft.sqlserver:mssql-jdbc:12.2.0.jre8') \
    .getOrCreate()

# Configurações do seu Fabric DW
server = 'jhzniwjaaxhunnvsq46v3jkd7y-2niwmv34mraullm7hds2kliywa.datawarehouse.fabric.microsoft.com'
database = 'lh_f1_lake_gold' # Ou o nome direto em string
table = 'dbo.abt_champions'

# String de conexão JDBC limpa
jdbc_url = f'jdbc:sqlserver://{server}:1433;database={database};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.datawarehouse.fabric.microsoft.com;loginTimeout=30;'

# 3. Executa a leitura no Spark usando o Token de Acesso obtido
df = spark.read \
    .format('jdbc') \
    .option('url', jdbc_url) \
    .option('driver', 'com.microsoft.sqlserver.jdbc.SQLServerDriver') \
    .option('dbtable', f'(SELECT * FROM {table}) as sub_query') \
    .option('accessToken', access_token) \
    .load()

df = df.toPandas()

# %%
file_path = DATA_PATH / 'abt_f1_drivers_champion.csv'

df.to_csv(file_path,
          index=False,
          sep=';')