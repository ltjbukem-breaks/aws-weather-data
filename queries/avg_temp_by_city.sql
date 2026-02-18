SELECT
    forecast_date,
    forecast_date + INTERVAL '7' DAY AS forecast_week_end,
    city,
    state,
    ROUND(AVG(temperature), 2) AS avg_temperature_F,
    MAX(temperature) AS max_temperature_F,
    MIN(temperature) AS min_temperature_F
FROM curated_weather_analytics
GROUP BY forecast_date, forecast_date + INTERVAL '7' DAY, city, state
ORDER BY avg_temperature_F DESC;