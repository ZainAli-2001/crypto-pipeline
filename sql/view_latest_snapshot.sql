CREATE OR REPLACE VIEW crypto_pipeline.latest_snapshot AS
SELECT *
FROM crypto_pipeline.crypto_hourly_records
WHERE snapshot_ts = (
  SELECT max(snapshot_ts) FROM crypto_pipeline.crypto_hourly_records
);