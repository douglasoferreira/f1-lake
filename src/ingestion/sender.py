# %%
import argparse
import os

from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
import dotenv
from tqdm import tqdm

dotenv.load_dotenv()

ONELAKE_DFS_URL = 'https://onelake.dfs.fabric.microsoft.com'
CREDENTIAL = DefaultAzureCredential()

WORKSPACE_ID = os.getenv('WORKSPACE_ID')
LAKEHOUSE_ID = os.getenv('LAKEHOUSE_ID')

DATA_PATH = Path(__file__).resolve().parent.parent.parent / 'data'

class Sender:

    def __init__(self, workspace_id, lakehouse_id):
        self.workspace_id = workspace_id
        self.lakehouse_id = lakehouse_id

        self.service_client = DataLakeServiceClient(account_url=ONELAKE_DFS_URL, credential=CREDENTIAL)
        self.file_system_client = self.service_client.get_file_system_client(file_system=workspace_id)

    def process_file(self, filename):

        file = filename.split('/')[-1]
        lakehouse_path = f'{self.lakehouse_id}/Files/Results/{file}'

        try:
            file_client = self.file_system_client.get_file_client(lakehouse_path)
            with open(filename, 'rb') as data:
                file_client.upload_data(data, overwrite=True)

        except Exception as err:
            print(err)
            return False
        
        os.remove(filename)
        return True
    
    def process_folder(self, folder):
        files = [i for i in os.listdir(folder) if i.endswith('.parquet')]
        for f in tqdm(files):
            self.process_file(os.path.join(folder, f))

# %%
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace_id', type=str, default=WORKSPACE_ID, help='ID do Workspace (GUID)')
    parser.add_argument('--lakehouse_id', type=str, default=LAKEHOUSE_ID, help='ID do Lakehouse (GUID)')
    parser.add_argument('--folder', type=str, default=str(DATA_PATH), help='Pasta local com os parquets')
    args = parser.parse_args()

    if args.workspace_id and args.lakehouse_id:
        send = Sender(args.workspace_id, args.lakehouse_id)
        send.process_folder(args.folder)

    else:
        print('Sem IDs definidos corretamente')