import requests
import json
from google.cloud import secretmanager
import polars as pl

# import streamlit as st
#  try to get data from financial modeling prep api

# @st.cache_data
def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        
        # st.error(f"Error fetching data from API: {e}")
        return None
    except json.JSONDecodeError as e:
        # st.error(f"Error decoding JSON response: {e}")
        return None



def access_gcp_secret_version(project_id:str, secret_id:str, version_id="latest")->str:
    
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")



if __name__ == "__main__":

    stocks = {'symbols': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.B', 'JPM', 'UNH'],
              'key':access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
                                              secret_id='financialmodelingprep')
            }
    # api_key = access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
    #                                     secret_id='financialmodelingprep')
    
    stock_q = stocks['symbols'][0]
    api_key = stocks['key']
    url = f"https://financialmodelingprep.com/stable/quote?query={stock_q}&limit=1&apikey={api_key}"
    data = fetch_data_from_api(url)
    print(data)