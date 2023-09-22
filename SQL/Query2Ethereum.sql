WITH coin_change_v AS (
                        SELECT
                        date,
                        coin_id,
                        json_data,
                        "current_price.usd",
                        LAG("current_price.usd", 1) OVER (PARTITION BY coin_id ORDER BY date) AS prev_price,
                        LAG("current_price.usd", 2) OVER (PARTITION BY coin_id ORDER BY date) AS prev_price_2,
                        LAG("current_price.usd", 3) OVER (PARTITION BY coin_id ORDER BY date) AS prev_price_3,
                        LAG("current_price.usd", -1) OVER (PARTITION BY coin_id ORDER BY date) AS post_price
                        FROM
                        coin_price_usd
                        where coin_id = 'ethereum'
                        and date between '2023-06-01T00:00:00' and '2023-06-30T00:00:00'
),
consecutive_drops_v AS (
                        SELECT date,
                        coin_id,
                        (cast(json_data as json) -> 'market_data' -> 'market_cap' -> 'usd')::text::numeric as market_cap_usd,
                        "current_price.usd",
                        prev_price,
                        prev_price_2,
                        prev_price_3,
                        post_price,
                        CASE WHEN "current_price.usd" < prev_price AND prev_price < prev_price_2 AND prev_price_2 < prev_price_3 THEN 1 ELSE 0 END AS consecutive_drop
                        FROM
                        coin_change_v
)
SELECT
coin_id,
AVG(post_price -"current_price.usd") AS avg_price_increase,
MAX(market_cap_usd) AS current_market_cap_usd
FROM consecutive_drops_v
WHERE
consecutive_drop = 1
GROUP BY
coin_id



