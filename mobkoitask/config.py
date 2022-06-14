import storage.local as local_storage
import db.postgres as pg
import transformation.index as transformations


exchange_rates_etl_config = {
  'url': 'https://open.er-api.com/v6/latest/CHF',
  'output_folder': './out/exchange_rates',
  'output_filename': 'chf-rates.json',
  'storage_func': local_storage.save_to_file,
  'transform_func': transformations.transform_exchange_rates,
  'persist_func': pg.persist_exchange_rates
}

binance_etl_config = {
  'url': 'https://api.binance.com/api/v3/ticker/price',
  'output_folder': './out/binance',
  'output_filename': 'tickers-price.json',
  'storage_func': local_storage.save_to_file,
  'transform_func': transformations.transform_binance_tickers,
  'persist_func': pg.persist_binance_tickers
}

db_config = {
  'host': 'postgresql',
  'user': 'postgres',
  'password': 'password',
  'dbname': 'mobkoi',
  'connection_retries': 3
}

strategies = [
  exchange_rates_etl_config,
  binance_etl_config
]
