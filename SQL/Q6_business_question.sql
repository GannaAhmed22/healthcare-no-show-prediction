-- Q6: Which medical specialty groups have the highest no-show rates?

SELECT
    pr.specialty_group,
    COUNT(*) AS total_appointments,
    SUM(a.no_show_flag) AS no_shows,
    ROUND(100.0 * SUM(a.no_show_flag) / COUNT(*), 1) AS no_show_rate
FROM appointments a
JOIN provider pr
    ON a.provider_id = pr.provider_id
GROUP BY pr.specialty_group
ORDER BY no_show_rate DESC;
