# %%
import os
import dotenv
import time
import datetime
from collect import CollectResults
from sender import Sender

dotenv.load_dotenv()
WORKSPACE_ID = os.getenv('WORKSPACE_ID')
LAKEHOUSE_ID  = os.getenv('LAKEHOUSE_ID')

while True:

    print('Iniciando processo ...')

    print('Coletando dados...')
    collect_data = CollectResults(years=[datetime.datetime.now().year])
    collect_data.process_years()

    print('Enviando dados ...')
    sender_data = Sender(workspace_id=WORKSPACE_ID, lakehouse_id=LAKEHOUSE_ID)
    sender_data.process_folder('data/')

    print('Iteração finalizada.')
    time.sleep(60*60*6)