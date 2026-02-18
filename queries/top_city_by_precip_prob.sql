SELECT
    city,
    state,
    forecast_date,
    forecast_date + INTERVAL '7' DAY AS forecast_week_end,
    ROUND(AVG(probabilityofprecipitation_value), 2) AS avg_precip_probability
FROM curated_weather_analytics
WHERE probabilityofprecipitation_value IS NOT NULL
GROUP BY city, state, forecast_date, forecast_date + INTERVAL '7' DAY
ORDER BY avg_precip_probability DESC
LIMIT 10;