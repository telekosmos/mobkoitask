import os
import requests
import psycopg2

conn = psycopg2.connect(host="localhost", user="postgres", password="p0stgr3s", dbname="mobkoi")

def get_api_data(url) -> requests.Response:
  r = requests.get(url)
  return r

def save_to_file(output_path, filename, content):
  os.makedirs(output_path, exist_ok=True)
  with open(f'{output_path}/{filename}', 'w') as f:
    f.write(content)

def transform_to_rows_exchange(json_resp):
  base_code = json_resp['base_code']
  utc_update = json_resp['time_last_update_utc']
  long_update = json_resp['time_last_update_unix']
  rows = [ (base_code, target_code, rate, long_update, utc_update) for target_code, rate in json_resp['rates'].items()]

  return rows

def save_to_db(rows):
  stmt = """
    INSERT INTO public.exchange_rates (base_code, target_code, rate, unix_update, utc_update)
    VALUES (%s, %s, %s, %s, %s)
  """
  cur = conn.cursor()
  for row in rows:
    cur.execute(stmt, row)

  conn.commit()
  print(f"persisted {len(rows)} rates")
  cur.close()
  conn.close()

url = 'https://open.er-api.com/v6/latest/CHF'
resp = get_api_data(url)
print(f"got data {resp.status_code}")
save_to_file('./out', 'exchange-rates.json', resp.text)
print("saved to file")
rows = transform_to_rows_exchange(resp.json())
print(f"converted to rows {len(rows)}")
save_to_db(rows)
print("end")
