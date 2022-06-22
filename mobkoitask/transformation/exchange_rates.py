import json

def transform(resp_data):
  json_resp = json.loads(resp_data)
  base_code = json_resp['base_code']
  utc_update = json_resp['time_last_update_utc']
  long_update = json_resp['time_last_update_unix']
  rows = [ (base_code, target_code, rate, long_update, utc_update) for target_code, rate in json_resp['rates'].items()]

  return rows
