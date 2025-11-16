import requests
import json
from google.cloud import secretmanager
import polars as pl

from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from connections.connections import fetch_data_from_api, access_gcp_secret_version



if __name__ == "__main__":


    stocks = {'symbols': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'AMD', 'NVDA', 'BRK.B', 'JPM', 'UNH','5253'],
              'key':access_gcp_secret_version(project_id='hardy-magpie-468509-t1', secret_id='financialmodelingprep')
            }
    # api_key = access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
    #                                     secret_id='financialmodelingprep')
    

    stock_q = stocks['symbols'][10]
    print(f'stock_q: {stock_q}')
    api_key = stocks['key']
    url = f"https://financialmodelingprep.com/stable/batch-quote?symbols=={stock_q}&apikey={api_key}"
    json_d = fetch_data_from_api(url)
    df = pl.DataFrame(json_d)
    print(df)