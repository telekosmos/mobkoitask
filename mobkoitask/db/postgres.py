import psycopg2

def get_connection(host='localhost', user='postgres', password='p0stgr3s', dbname='mobkoi', retries=3):
  conn = None
  retry_counter = 0
  while retry_counter < retries:
    try:
      conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
    except psycopg2.OperationalError:
      continue
    break;

  if retry_counter == retries:
    raise psycopg2.OperationalError
  else:
    return conn


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
