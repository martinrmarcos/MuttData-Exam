CREATE VIEW CoinChange AS
SELECT
date,
coin_id,
json_data,
"current_price.usd",
LAG("current_price.usd", 1) OVER (PARTITION BY coin_id ORDER BY date) AS prev_price,
LAG("current_price.usd", 2) OVER (PARTITION BY coin_id ORDER BY date) AS prev_price_2,
LAG("current_price.usd", 3) OVER (PARTITION BY coin_id ORDER BY date) AS prev_price_3
FROM
coin_price_usd
where coin_id = 'ethereum'
and date between '2023-06-01T00:00:00' and '2023-06-30T00:00:00'



CREATE VIEW ConsecutiveDrops AS
SELECT date,
coin_id,
(cast(json_data as json) -> 'market_data' -> 'market_cap' -> 'usd')::text::bigint as market_cap_usd,
"current_price.usd",
prev_price,
prev_price_2,
prev_price_3,
CASE WHEN "current_price.usd" < prev_price AND prev_price < prev_price_2 AND prev_price_2 < prev_price_3 THEN 1 ELSE 0 END AS consecutive_drop
FROM
CoinChange

CREATE VIEW AveragePriceIncrease AS
SELECT
coin_id,
AVG("current_price.usd" - prev_price) AS avg_price_increase,
MAX(market_cap_usd) AS current_market_cap_usd
FROM ConsecutiveDrops
WHERE
consecutive_drop = 1
GROUP BY
coin_id

SELECT
AVG(avg_price_increase) AS overall_avg_price_increase,
coin_id,
current_market_cap_usd
FROM
AveragePriceIncrease
GROUP BY
coin_id, current_market_cap_usd




select * from CoinChange

DROP VIEW AveragePriceIncrease;
DROP VIEW ConsecutiveDrops;
DROP VIEW CoinChange;
