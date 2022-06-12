from re import split
from datetime import datetime
import requests
from psycopg2 import OperationalError, Error

import db.postgres as pg
from config import db_config, strategies

def get_api_data(url):
  r = requests.get(url)
  return r

def process_etl():
  def build_filename(filename, suffix):
    [name, ext] = split('\\.', filename)
    output_filename = f'{name}{suffix}.{ext}'
    return output_filename

  def process_etl_strategies(file_suffix):
    conn = pg.get_connection(db_config['host'], db_config['user'], db_config['password'], db_config['dbname'])
    for strategy in strategies:
      resp = requests.get(strategy['url'])
      if resp.status_code == 200:
        print(f"Got data from {strategy['url']}")
        storage_func = strategy['storage_func']
        output_filename = build_filename(strategy['output_filename'], file_suffix)
        storage_func(strategy['output_folder'], output_filename, resp.text)
        print("Saved to file")
        rows = strategy['transform_func'](resp)
        print(f"Transformed to persist {len(rows)} rows")
        strategy['persist_func'](conn, rows)
        print(f"Successfully persisted {len(rows)} rows")
      else:
        print(f'Error on request {strategy["url"]}: {resp.status_code}')

    conn.close()

  try:
    file_suffix = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    process_etl_strategies(file_suffix)
  except OperationalError:
    print(f'Could not connect to database: {db_config}')
  except Error as pg_ex:
    print(f'Database error: {pg_ex.diag.message_detail}')
  except requests.RequestException as req_ex:
    print(f'HTTP request error - URL: {strategy["url"]}')


process_etl()
