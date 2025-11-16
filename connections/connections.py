import requests
import json
from google.cloud import secretmanager
import polars as pl

from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

# import streamlit as st
#  try to get data from financial modeling prep api

# @st.cache_data
def fetch_data_from_api(api_url)->dict:
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        # st.error(f"Error fetching data from API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error fetching data from API: {e}")
        # st.error(f"Error decoding JSON response: {e}")
        return None



def access_gcp_secret_version(project_id:str, secret_id:str, version_id="latest")->str:
    
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def access_gcp_secret_version_dict(project_id:str, secret_id:str, version_id="latest")->dict:
    
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": name})
    secret_string = response.payload.data.decode("UTF-8")
    secret_dict = json.loads(secret_string)
    return secret_dict

def getconn(creds_content:dict):
    """Create a connection to Cloud SQL PostgreSQL"""
    connector = Connector(ip_type=IPTypes.PUBLIC)
    conn = connector.connect(
        creds_content['instance_connection_name'],
        "pg8000",  # PostgreSQL driver
        user=creds_content['db_user'],
        password=creds_content['db_password'],
        db=creds_content['db_name']
    )
    return conn

# engine = sqlalchemy.create_engine(
#     "postgresql+pg8000://",
#     creator=getconn,
# )

# return engine


# engine = sqlalchemy.create_engine(
#     "postgresql+pg8000://",
#     creator=getconn,
# )


# if __name__ == "__main__":

#     stocks = {'symbols': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'AMD', 'NVDA', 'BRK.B', 'JPM', 'UNH'],
#               'key':access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
#                                               secret_id='financialmodelingprep')
#             }
#     # api_key = access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
#     #                                     secret_id='financialmodelingprep')
    

#     stock_q = stocks['symbols'][7]
#     api_key = stocks['key']
#     print(f'api_key: {api_key}')
#     url = f"https://financialmodelingprep.com/stable/quote?symbol={stock_q}&apikey={api_key}"
#     # json_data = fetch_data_from_api(url)
#     # print(f'data: {json_data[0]}')

    
#     # res = access_gcp_secret_version(project_id='hardy-magpie-468509-t1',secret_id='mycloudsql')
#     # print(res)
#     # df = pl.DataFrame(json_data[0])
#     # print(df)

