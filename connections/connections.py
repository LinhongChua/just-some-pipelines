import requests
import json
from google.cloud import secretmanager
import polars as pl

from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

# import streamlit as st
#  try to get data from financial modeling prep api

# @st.cache_data
def fetch_data_from_api(api_url):
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

# initialize Cloud SQL Connector
# connector = Connector()

# SQLAlchemy database connection creator function
# def getconn(pw):
#     conn = connector.connect(
#         "", # Cloud SQL Instance Connection Name
#         "pg8000",
#         user="",
#         password=pw,
#         db="postgres",
#         ip_type=IPTypes.PUBLIC # IPTypes.PRIVATE for private IP
#     )
#     return conn

# # create SQLAlchemy connection pool
# pool = sqlalchemy.create_engine(
#     "postgresql+pg8000://",
#     creator=getconn,
# )

# # interact with Cloud SQL database using connection pool
# with pool.connect() as db_conn:
#     # query database
#     result = db_conn.execute("SELECT * from my_table").fetchall()

#     # Do something with the results
#     for row in result:
#         print(row)

# # close Cloud SQL Connector
# connector.close()

# def getconnection():
    



if __name__ == "__main__":

    stocks = {'symbols': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'AMD', 'NVDA', 'BRK.B', 'JPM', 'UNH'],
              'key':access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
                                              secret_id='financialmodelingprep')
            }
    # api_key = access_gcp_secret_version(project_id='hardy-magpie-468509-t1', 
    #                                     secret_id='financialmodelingprep')
    

    stock_q = stocks['symbols'][7]
    api_key = stocks['key']
    print(f'api_key: {api_key}')
    url = f"https://financialmodelingprep.com/stable/quote?symbol={stock_q}&apikey={api_key}"
    # json_data = fetch_data_from_api(url)
    # print(f'data: {json_data[0]}')

    
    # res = access_gcp_secret_version(project_id='hardy-magpie-468509-t1',secret_id='mycloudsql')
    # print(res)
    # df = pl.DataFrame(json_data[0])
    # print(df)

# ===== CONFIGURATION =====
PROJECT_ID = ""
REGION = "asia-southeast1"
INSTANCE_NAME = ""
INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = "postgres"

# ===== CONNECTION =====
connector = Connector()

def getconn():
    """Create a connection to Cloud SQL PostgreSQL"""
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",  # PostgreSQL driver
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )
    return conn

engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# ===== TEST CONNECTION =====
try:
    # Test with a simple DataFrame
    test_df = pl.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"]
    })
    
    test_df.write_database(
        table_name="test_table",
        connection=engine,
        if_table_exists="replace"
    )
    
    print("✅ Connection successful!")
    print(f"✅ Loaded {len(test_df)} rows to Cloud SQL PostgreSQL 15")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    
finally:
    connector.close()