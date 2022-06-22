from datetime import datetime
import json

def transform(resp_data):
  json_resp = json.loads(resp_data)
  rows = [ (elem['symbol'], elem['price']) for elem in json_resp ]

  return rows
