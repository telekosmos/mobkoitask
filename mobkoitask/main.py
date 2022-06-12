import requests
import db.postgres as pg
from config import db_config, strategies

def get_api_data(url):
  r = requests.get(url)
  return r

def process_etl():
  conn = pg.get_connection(db_config['host'], db_config['user'], db_config['password'], db_config['dbname'])
  for strategy in strategies:
    resp = get_api_data(strategy['url'])
    print(f"got data {resp.status_code}")
    storage_func = strategy['storage_func']
    storage_func(strategy['output_folder'], strategy['output_filename'], resp.text)
    print("saved to file")
    rows = strategy['transform_func'](resp)
    print(f"converted to rows {len(rows)}")
    strategy['persist_func'](conn, rows)
    print(f"persisted {len(rows)} rates")

  conn.close()

process_etl()
