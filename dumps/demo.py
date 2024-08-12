

import os
from dotenv import load_dotenv

load_dotenv()

# crazy stuff but config is loaded as soon as you  import load config so loaddotenv won't get a chance to change pyicebrg home
# if i import load catalog before  invoking load_dotenv
from pyiceberg.catalog import load_catalog

print('checking...')
print(os.environ.get('PYICEBERG_HOME'))

# os.environ['PYICEBERG_HOME'] ='/Users/emmanuelogunwede/code_space/open_source/hacking-apache-iceberg/src'
# os.environ['PYICEBERG_CATALOG__HIVE-CATALOG__URI'] = 'thrift://hive-metastore:9083'

catalog = load_catalog('hive-catalog')


ns = catalog.list_namespaces()

print(ns)

# catalog.create_namespace('dev_emmanuel')