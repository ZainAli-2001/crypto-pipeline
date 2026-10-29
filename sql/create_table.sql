CREATE EXTERNAL TABLE crypto_pipeline.crypto_hourly_records (
  snapshot_ts timestamp,
  id string,
  symbol string,
  name string,
  market_cap_rank bigint,
  current_price double,
  market_cap double,
  fully_diluted_valuation double,
  total_volume double,
  high_24h double,
  low_24h double,
  price_change_24h double,
  price_change_percentage_24h double,
  market_cap_change_24h double,
  market_cap_change_percentage_24h double,
  circulating_supply double,
  total_supply double,
  max_supply double,
  ath double,
  ath_change_percentage double,
  ath_date timestamp,
  atl double,
  atl_change_percentage double,
  atl_date timestamp,
  last_updated timestamp,
  price_change_percentage_1h_in_currency double,
  price_change_percentage_24h_in_currency double,
  price_change_percentage_7d_in_currency double
)
PARTITIONED BY (dt string)
STORED AS PARQUET
LOCATION 's3://<DATA_BUCKET>/curated/'
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.dt.type' = 'date',
  'projection.dt.format' = 'yyyy-MM-dd',
  'projection.dt.range' = '2026-10-28,NOW',
  'projection.dt.interval' = '1',
  'projection.dt.interval.unit' = 'DAYS',
  'storage.location.template' = 's3://<DATA_BUCKET>/curated/dt=${dt}/'
);