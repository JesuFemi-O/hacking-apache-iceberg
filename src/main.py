from dotenv import load_dotenv

load_dotenv()

from pyiceberg.exceptions import NamespaceAlreadyExistsError, NoSuchTableError
import pyarrow.parquet as pq
import pandas as pd
from pyiceberg.catalog import load_catalog
# from pyiceberg.io.pandas import pandas_to_iceberg

# Configuration for Hive Catalog
hive_metastore_uri = 'thrift://localhost:9083'  # URI for the Hive Metastore
warehouse_uri = 's3://datalake/'
s3_access_key = 'minio'
s3_secret_key = 'minio123'

trip_data_path = '../data/yellow_tripdata_2023-01.parquet'

catalog = load_catalog('hive-catalog')


# Create namespace if it doesn't exist
try:
    catalog.create_namespace('dev_emmanuel')
except NamespaceAlreadyExistsError:
    pass


tbl_taxis = pq.read_table(trip_data_path)

try:
    catalog.drop_table('dev_emmanuel.taxis')
except NoSuchTableError:
    pass

taxis_iceberg_table = catalog.create_table(
    'dev_emmanuel.taxis',
    schema=tbl_taxis.schema
)

print("Iceberg table created successfully")

taxis_iceberg_table.append(tbl_taxis)

print("successfully wrote data to table...")