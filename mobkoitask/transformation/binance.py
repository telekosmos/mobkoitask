from datetime import datetime
import calendar

def transform(resp):
  json_resp = resp.json()
  # utcnow = datetime.utcnow()
  # utc_time = calendar.timegm(utcnow.timetuple())
  rows = [ (elem['symbol'], elem['price']) for elem in json_resp ]

  return rows
