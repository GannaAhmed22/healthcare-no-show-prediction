-- Q7: Do weekends, holidays, and flu season change the no-show rate?

SELECT
    CASE WHEN c.weekend_flag = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    CASE WHEN c.holiday_flag = 1 THEN 'Holiday' ELSE 'Normal day' END AS holiday,
    CASE WHEN c.flu_season_flag = 1 THEN 'Flu season' ELSE 'Off season' END AS flu_season,
    COUNT(*) AS total_appointments,
    SUM(a.no_show_flag) AS no_shows,
    ROUND(100.0 * SUM(a.no_show_flag) / COUNT(*), 1) AS no_show_rate
FROM appointments a
JOIN calendar c
    ON a.appointment_date = c.calendar_date
GROUP BY day_type, holiday, flu_season
ORDER BY no_show_rate DESC;
