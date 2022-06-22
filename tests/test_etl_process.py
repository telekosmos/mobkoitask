
import json
from mobkoitask.config import etl_binance_config, db_config
from mobkoitask.etl_process import run as process_etl
from unittest import mock

class MockResponse():
  def __init__(self, status_code, content):
    self.status_code = status_code
    self.text = content

@mock.patch("psycopg2.connect")
@mock.patch("requests.get")
@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("os.makedirs")
def test_binance_etl(mock_makedirs, mock_file, mock_request, mock_pg_connect):
  # mock_file.return_value.write.return_value = None
  mock_file_write = mock_file.return_value.write
  mock_file_write.return_value = None
  mock_makedirs.return_value = None

  cur = mock.MagicMock(name="my_cursor")
  cur.return_value.execute.return_value = None
  cnxn = mock.MagicMock(name="pg_connection")
  cnxn.cursor.return_value.__enter__.return_value = cur
  cnxn.close.return_value = None
  mock_pg_connect.return_value = cnxn

  binance_tickers_resp_fixture = """
    [
      {
        "symbol": "ETHBTC",
        "price": "0.05353600"
      },
      {
        "symbol": "LTCBTC",
        "price": "0.00182000"
      },
      {
        "symbol": "BNBBTC",
        "price": "0.00941200"
      },
      {
        "symbol": "NEOBTC",
        "price": "0.00039900"
      },
      {
        "symbol": "QTUMETH",
        "price": "0.00220900"
      }]
  """
  mock_request.return_value = MockResponse(200, binance_tickers_resp_fixture)

  strategies = [etl_binance_config]
  process_etl(db_config, strategies)

  mock_request.assert_called_with(etl_binance_config.url)
  assert mock_file.call_count == 1
  assert mock_pg_connect.call_count == 1
  assert cur.execute.call_count == 5
  assert cnxn.close.call_count == 1
  assert mock_makedirs.call_count == 1

def test_malformed_url():
  pass

def test_db_no_connection():
  pass
