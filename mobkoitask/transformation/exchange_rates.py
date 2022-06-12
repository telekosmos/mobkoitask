
def transform(resp):
  json_resp = resp.json()
  base_code = json_resp['base_code']
  utc_update = json_resp['time_last_update_utc']
  long_update = json_resp['time_last_update_unix']
  rows = [ (base_code, target_code, rate, long_update, utc_update) for target_code, rate in json_resp['rates'].items()]

  return rows
