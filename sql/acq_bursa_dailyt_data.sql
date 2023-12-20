CREATE TABLE IF NOT EXISTS `winter-anchor-259905.stock_data.acq_bursa_daily_data` (
    date DATE,
    stock_code STRING,
    stock_name STRING,
    currency STRING,
    open FLOAT64,
    high FLOAT64,
    low FLOAT64,
    close FLOAT64,
    volume INT64,
    market_transaction_value INT64,
    ingestion_date DATE
) 
PARTITION BY date
CLUSTER BY stock_code, stock_name;