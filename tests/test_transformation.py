from functools import reduce
import json
import mobkoitask.transformation.index as transformations
from unittest.mock import MagicMock, Mock

def test_transform_exchange_rates():
  exchange_rates_resp_fixture = """
    {"result":"success","provider":"https://www.exchangerate-api.com","documentation":"https://www.exchangerate-api.com/docs/free","terms_of_use":"https://www.exchangerate-api.com/terms","time_last_update_unix":1654992151,"time_last_update_utc":"Sun, 12 Jun 2022 00:02:31 +0000","time_next_update_unix":1655079501,"time_next_update_utc":"Mon, 13 Jun 2022 00:18:21 +0000","time_eol_unix":0,"base_code":"CHF","rates":{"CHF":1,"AED":3.72,"AFN":90.74,"ALL":114.25,"AMD":428.28}}
  """
  mock_json_resp = json.loads(exchange_rates_resp_fixture)

  mock_resp = Mock()
  mock_resp.json.return_value = mock_json_resp

  rows = transformations.transform_exchange_rates(mock_resp)
  assert len(rows) == 5
  base_codes = [ row[0] == 'CHF' for row in rows ]
  assert reduce(lambda accum, e: accum and e, base_codes, True) == True
  assert reduce(lambda accum, e: accum and e == 5, [ len(row) for row in rows ], True)
