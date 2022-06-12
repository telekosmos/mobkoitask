import psycopg2

def get_connection(host='localhost', user='postgres', password='p0stgr3s', dbname='mobkoi'):
  return psycopg2.connect(host=host, user=user, password=password, dbname=dbname)

def persist_exchange_rates(conn, rows):
  stmt = """
    INSERT INTO public.exchange_rates (base_code, target_code, rate, unix_update, utc_update)
    VALUES (%s, %s, %s, %s, %s)
  """
  with conn:
    with conn.cursor() as cur:
      for row in rows:
        cur.execute(stmt, row)

def persist_binance_tickers(conn, rows):
  stmt = """
    INSERT INTO public.binance_tickers (symbol, price)
    VALUES (%s, %s)
  """
  with conn:
    with conn.cursor() as cur:
      for row in rows:
        cur.execute(stmt, row)
