SELECT
    city,
    state,
    forecast_date,
    forecast_date + INTERVAL '7' DAY AS forecast_week_end,
    winddirection,
    ROUND(AVG(CAST(regexp_extract(windspeed, '([0-9]+)', 1) AS INTEGER)), 2) AS avg_wind_speed_mph
FROM curated_weather_analytics
WHERE winddirection IS NOT NULL AND trim(winddirection) <> ''
GROUP BY city, state, forecast_date, forecast_date + INTERVAL '7' DAY, winddirection
ORDER BY avg_wind_speed_mph DESC;