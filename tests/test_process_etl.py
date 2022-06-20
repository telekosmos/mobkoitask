
from requests import patch
# from mobkoitask.config import etl_binance_config, db_config
from mobkoitask.main import process_etl
from unittest import mock

@patch("psycopg2.connect")
@patch("requests.get")
@patch("builtins.open", new_callable=mock.mock_open, read_data="data")
def test_binance_etl(mock_file, mock_request, mock_pg_connect):
  mock_file.write.return_value = None

  cursor = mock.MagicMock(name="my_cursor")
  cursor.execute.return_value = None
  cnxn = mock.MagicMock("pg_connection")
  cnxn.cursor.return_value = cursor
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
  mock_request.text.return_value = binance_tickers_resp_fixture
  mock_request.status_code.return_value = 200

  strategies = [etl_binance_config]
  process_etl(db_config, strategies)

  mock_request.assert_called_with(etl_binance_config.url)
  pass

def test_malformed_url():
  pass

def test_db_no_connection():
  pass
