# %%
import dotenv
import os
import argparse
from azure.storage.blob import BlobServiceClient
from tqdm import tqdm

dotenv.load_dotenv()

AZ_CONN_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

class Sender:

    def __init__(self, container_name, container_folder):
        self.container_name = container_name
        self.container_folder = container_folder
        blob_service_client = BlobServiceClient.from_connection_string(AZ_CONN_STR)
        self.container_client = blob_service_client.get_container_client(container_name)

    def process_file(self, filename):

        file = filename.split('/')[-1]
        container_path = os.path.join(self.container_folder, file)

        try:
            with open(filename, 'rb') as data:
                self.container_client.upload_blob(container_path, 
                                            data, 
                                            overwrite=True)

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
if __name__ == 'main':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--container', type=str)
    parser.add_argument('--container_path', default='f1/results', type=str)
    parser.add_argument('--folder', default='data', type=str)
    args = parser.parse_args()

    if args.container:
        send = Sender('f1-lake', 'f1-lake/results')
        send.process_folder(args.folder)

    else:
        print('Sem container definido')