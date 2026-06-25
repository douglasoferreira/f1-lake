# %%
import os
import dotenv
import time
import datetime
from collect import CollectResults
from sender import Sender

dotenv.load_dotenv()
AZ_CONT_NAM = os.getenv('AZURE_CONTAINER_NAME')
AZ_CONT_FDR = os.getenv('AZURE_CONTAINER_FOLDER')

while True:

    print('Iniciando processo ...')

    print('Coletando dados...')
    collect_data = CollectResults(years=[datetime.datetime.now().year])
    collect_data.process_years()

    print('Enviando dados ...')
    sender_data = Sender(container_name=AZ_CONT_NAM, container_folder=AZ_CONT_FDR)
    sender_data.process_folder('data/')

    print('Iteração finalizada.')
    time.sleep(60*60*6)