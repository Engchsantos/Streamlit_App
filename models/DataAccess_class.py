import pandas as pd
from google.cloud import firestore
import tomli
import tempfile
import json

class DataAccess:
    def __init__(self):
        pass

    def get_brent_data(self):
        return pd.read_csv('data/df.csv')
    
    def get_brent_data_firebase(self, data_inicial):
        with open(".streamlit/secrets.toml", "rb") as toml_file:
            toml_data = tomli.load(toml_file)

        # Converter TOML para JSON
        json_data = json.dumps(toml_data)
        # Criar um arquivo temporário com as credenciais JSON
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_json_file:
            temp_json_file.write(json_data)
            temp_json_path = temp_json_file.name
        client = firestore.Client.from_service_account_json(temp_json_path)
        collection_name = "petroleo_brent"
        data_list = []
        
        try:
            query = client.collection(collection_name).where("data", ">", pd.to_datetime(data_inicial))
            docs = query.stream()
            
            for doc in docs:
                doc_data = doc.to_dict()
                data_list.append(doc_data)
            
            # Criar DataFrame com os dados filtrados
            df = pd.DataFrame(data_list)
            df.rename(columns={'valor': 'y', 'data': 'ds'}, inplace=True)
            df['ds'] = pd.to_datetime(df['ds'], format="%Y-%m-%d", errors="coerce").dt.date
            df['y'] = pd.to_numeric(df['y'])
            df.sort_values(by='ds', ascending=False, inplace=True)
            df.reset_index(drop=True, inplace=True)
            return df
        except Exception as e:
            print(f"Erro ao acessar o Firestore: {e}")
            return None
