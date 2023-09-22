
CREATE TABLE IF NOT EXISTS coin_price_usd (
    date TIMESTAMP,
    "current_price.usd" NUMERIC,
    coin_id VARCHAR(255),
    json_data JSON
);


CREATE TABLE IF NOT EXISTS maxmin_monthly_usd (
    coin_id VARCHAR(255),
    max_price NUMERIC,
    min_price NUMERIC,
    month NUMERIC,
    year NUMERIC
);
