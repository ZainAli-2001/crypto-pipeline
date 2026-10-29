CREATE OR REPLACE VIEW crypto_pipeline.top_losers AS
SELECT market_cap_rank, symbol, name, current_price,
       price_change_percentage_24h, total_volume
FROM crypto_pipeline.latest_snapshot
WHERE price_change_percentage_24h IS NOT NULL
ORDER BY price_change_percentage_24h ASC
LIMIT 10;
