-- Q5: How do transportation barriers, distance, and geographical deprivation
--     interact to influence appointment attendance?

WITH grouped AS (
    SELECT
        CASE WHEN transportation_barrier_flag = 1 THEN 'Has barrier'
             ELSE 'No barrier' END AS transport_barrier,

        CASE WHEN distance_to_clinic_miles < 5  THEN '1) < 5 miles'
             WHEN distance_to_clinic_miles < 10 THEN '2) 5-10 miles'
             WHEN distance_to_clinic_miles < 20 THEN '3) 10-20 miles'
             ELSE '4) 20+ miles' END AS distance_band,

        -- quintile 5 has very few rows so we merged it with 4
        CASE WHEN deprivation_quintile IN (1, 2) THEN '1) Low'
             WHEN deprivation_quintile = 3       THEN '2) Medium'
             ELSE '3) High' END AS deprivation_level,

        no_show_flag
    FROM fact_appointments
)
SELECT
    transport_barrier,
    distance_band,
    deprivation_level,
    COUNT(*) AS total_appointments,
    SUM(no_show_flag) AS no_shows,
    ROUND(100.0 * SUM(no_show_flag) / COUNT(*), 1) AS no_show_rate
FROM grouped
GROUP BY transport_barrier, distance_band, deprivation_level
HAVING COUNT(*) >= 30
ORDER BY no_show_rate DESC;
