-- Q9: Are telehealth and same-day appointments missed less than in-person appointments booked in advance?

SELECT
    CASE WHEN telehealth_flag = 1 THEN 'Telehealth' ELSE 'In-person' END AS visit_mode,
    CASE WHEN same_day_flag = 1 THEN 'Same day' ELSE 'Booked in advance' END AS booking,
    COUNT(*) AS total_appointments,
    SUM(no_show_flag) AS no_shows,
    ROUND(100.0 * SUM(no_show_flag) / COUNT(*), 1) AS no_show_rate
FROM appointments
GROUP BY visit_mode, booking
HAVING COUNT(*) >= 30
ORDER BY no_show_rate DESC;
