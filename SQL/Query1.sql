

select coin_id, EXTRACT(MONTH FROM date) AS month, EXTRACT(YEAR FROM date) AS year, avg("current_price.usd") AS avgpricepermonth
FROM coin_price_usd
GROUP BY coin_id, EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
ORDER BY coin_id, year desc, month desc