-- Q8: Which facility types and locations (urban or rural) have the most missed appointments?

SELECT
    f.facility_type,
    f.urban_rural_group,
    COUNT(*) AS total_appointments,
    SUM(a.no_show_flag) AS no_shows,
    ROUND(100.0 * SUM(a.no_show_flag) / COUNT(*), 1) AS no_show_rate
FROM appointments a
JOIN facility f
    ON a.facility_id = f.facility_id
GROUP BY f.facility_type, f.urban_rural_group
HAVING COUNT(*) >= 30
ORDER BY no_show_rate DESC;
