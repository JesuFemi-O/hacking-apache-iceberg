# Talking to Iceberg from python

There seem to be many quirky stuff about the pyiceberg library at the moment.

If you're not willing to keep your pyiceberg.yaml file in your home directory for any reason like checking it into version control (you really shouldn't do this in production setups!!) you'll probably have a tough time getting the library correctly parsing your env settings and using them.

There's a weird thing in the library load_catalog api such that the config is eagerly loaded as soon as you import that library instead of it being loaded at the point where you invoke the api, because of this weirdness, I've had to import load_dotenv and invoke it before importing anything from pyiceberg else it doesn't work!

in production environment I think my preferance for loading a catalog will be to directly invoke the catalog directly in code instead of letting the weird pyiceberg code do it for me, it really sucks right now...

also the docs left me under the impression that simply setting the metastore uri would be enough info for my catalog config but that's not true, I had to explicitly provide all my s3 config to the catalog property object to get it working correctly.

my ideal prod code would probably look like this:

```python
from dotenv import load_dotenv
import os

load_dotenv()

from pyiceberg.catalog.hive import HiveCatalog
from pyiceberg.exceptions import NamespaceAlreadyExistsError, NoSuchTableError
import pyarrow.parquet as pq
import pandas as pd

# Configuration for Hive Catalog
hive_metastore_uri = 'thrift://localhost:9083'  # URI for the Hive Metastore
warehouse_uri = os.envrion.get('MINIO_WAREHOUSE','s3://datalake/')
s3_access_key = os.envrion.get('MINIO_ACCESS_KEY','minio')
s3_secret_key = os.envrion.get('MINIO_ACCESS_SECRET_KEY','minio123')
region= os.environ.get(MINIO_REGION, 'local')

trip_data_path = '../data/yellow_tripdata_2023-01.parquet'

# Instantiate the HiveCatalog directly
catalog = HiveCatalog(
    name="hive",
    uri=hive_metastore_uri,
    warehouse=warehouse_uri,
    properties={
        "s3.endpoint": "http://localhost:9000",  # Minio endpoint
        "s3.access-key-id": s3_access_key,       # Minio access key
        "s3.secret-access-key": s3_secret_key,   # Minio secret key
        "s3.region": region,                     # Region Value (doesn't matter for Minio but should match)
        "s3.path-style-access": "true",          # Important for Minio
    }
)

# Create namespace if it doesn't exist
try:
    catalog.create_namespace('dev_emmanuel')
except NamespaceAlreadyExistsError:
    pass

# Load the Parquet file as a PyArrow table
tbl_taxis = pq.read_table(trip_data_path)

# Drop the table if it exists
try:
    catalog.drop_table('dev_emmanuel.taxis')
except NoSuchTableError:
    pass

# Create a new Iceberg table in the Hive catalog
taxis_iceberg_table = catalog.create_table(
    identifier='dev_emmanuel.taxis',
    schema=tbl_taxis.schema
)

print("Iceberg table created successfully")

# Assuming taxis_iceberg_table is the table object
# and using the append function to insert data
taxis_iceberg_table.append(tbl_taxis)

print("Successfully wrote data to table...")

```

I've done a full load here, I'll love to see what an incremental load would look like next and then we can start rolling in tools like dagster and dlthub