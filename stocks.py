import requests
import json
from google.cloud import secretmanager
import polars as pl

from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy


if __name__ == "__main__":


    stocks = {'symbols': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'AMD', 'NVDA', 'BRK.B', 'JPM', 'UNH'],
              'key':access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
                                              secret_id='financialmodelingprep')
            }
    # api_key = access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
    #                                     secret_id='financialmodelingprep')
    

    stock_q = stocks['symbols'][7]
    api_key = stocks['key']
    url = f"https://financialmodelingprep.com/stable/quote?symbol={stock_q}&apikey={api_key}"