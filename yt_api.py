
import json
from google.cloud import secretmanager
import polars as pl

from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from connections.connections import fetch_data_from_api, access_gcp_secret_version

if __name__ == "__main__":
    print('hello world')