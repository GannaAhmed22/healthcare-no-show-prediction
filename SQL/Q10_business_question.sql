-- Q10: Does bad weather on the appointment day affect in-person visits more than telehealth visits?

SELECT
    weather_severity_group,
    CASE WHEN telehealth_flag = 1 THEN 'Telehealth' ELSE 'In-person' END AS visit_mode,
    COUNT(*) AS total_appointments,
    SUM(no_show_flag) AS no_shows,
    ROUND(100.0 * SUM(no_show_flag) / COUNT(*), 1) AS no_show_rate
FROM appointments
GROUP BY weather_severity_group, visit_mode
ORDER BY weather_severity_group, visit_mode;
