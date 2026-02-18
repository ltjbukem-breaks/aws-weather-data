CREATE OR REPLACE VIEW curated_weather_analytics AS
SELECT city, state, name, 
       from_unixtime(starttime / 1000000000) as start_time,
       from_unixtime(endtime / 1000000000) as end_time,
       temperature, temperatureunit,
       shortforecast, detailedforecast, 
       windspeed, winddirection, 
       probabilityofprecipitation_value, 
       CAST(
        date_parse(concat(year, '-', month, '-', day), '%Y-%m-%d')
        AS date
    ) AS forecast_date
FROM curated;
