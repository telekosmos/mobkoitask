from re import split
from datetime import datetime
import requests
from psycopg2 import OperationalError, Error

import mobkoitask.db.postgres as pg
# from mobkoitask.config import db_config, etl_strategies

def get_api_data(url):
  r = requests.get(url)
  return r

def run(db_config, etls_config):
  def build_filename(filename, suffix):
    [name, ext] = split('\\.', filename)
    output_filename = f'{name}{suffix}.{ext}'
    return output_filename

  def process_etl_strategy(db_cfg, strategy, file_suffix):
    print(f"Connecting to postgres with credentials {db_cfg}...")
    resp = requests.get(strategy.url)
    if resp.status_code == 200:
      print(f"Got data from {strategy.url}")
      conn = pg.get_connection(db_cfg.host, db_cfg.user, db_cfg.password, db_cfg.dbname)
      storage_func = strategy.storage_func
      output_filename = build_filename(strategy.output_filename, file_suffix)
      storage_func(strategy.output_folder, output_filename, resp.text)
      print("Saved to file")
      rows = strategy.transform_func(resp.text)
      print(f"Transformed to persist {len(rows)} rows")
      strategy.persist_func(conn, rows)
      print(f"Successfully persisted {len(rows)} rows")
      conn.close()
    else:
      print(f'Error on request {strategy.url}: {resp.status_code}')

  try:
    file_suffix = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    for etl_strategy in etls_config:
      process_etl_strategy(db_config, etl_strategy, file_suffix)
  except OperationalError as e:
    print(f'Could not connect to database: {db_config} -> {e}')
  except Error as pg_ex:
    print(f'Database error: {pg_ex.diag.message_detail}')
  except requests.RequestException as req_ex:
    print(f'HTTP request error - URL: {req_ex.errno}')
