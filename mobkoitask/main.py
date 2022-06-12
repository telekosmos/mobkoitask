from sqlite3 import OperationalError
import requests
from psycopg2 import OperationalError, Error
import db.postgres as pg
from config import db_config, strategies

def get_api_data(url):
  r = requests.get(url)
  return r

def process_etl():
  def process_etl_strategies():
    conn = pg.get_connection(db_config['host'], db_config['user'], db_config['password'], db_config['dbname'])
    for strategy in strategies:
      resp = get_api_data(strategy['url'])
      if resp.status_code == 200:
        print(f"got data {resp.status_code}")
        storage_func = strategy['storage_func']
        storage_func(strategy['output_folder'], strategy['output_filename'], resp.text)
        print("saved to file")
        rows = strategy['transform_func'](resp)
        print(f"converted to rows {len(rows)}")
        strategy['persist_func'](conn, rows)
        print(f"persisted {len(rows)} rates")
      else:
        print(f'Error on request {strategy["url"]}: {resp.status_code}')

    conn.close()

  try:
    process_etl_strategies()
  except OperationalError:
    print(f'Could not connect to database: {db_config}')
  except Error as pg_ex:
    print(f'Database error: {pg_ex.diag.message_detail}')
  except requests.RequestException as req_ex:
    print(f'HTTP request error - URL: {strategy["url"]}')


process_etl()
