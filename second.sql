--PostgreSQL 9.6
--'\\' is a delimiter

-- Для этой задачи нашёл в интернете вашу статью и пользовался ей как основой http://leftjoin.ru/page-3/
-- не совсем только понял, почему там выполняется reg LEFT JOIN cohort, ведь левая таблица меньше правой, 
-- и значения из правой таблицы теряются
-- формат дат тоже не указывал, оставил их по умолчанию
SELECT EXTRACT(MONTH FROM installed_table.installed_at) as installed_month,
    SUM(retention_table.count_unique_user_retention) / SUM(installed_table.count_unique_user_install) as retention
FROM 
    (SELECT user.installed_at as installed_at,
        COUNT (DISTINCT user.user_id) as count_unique_user_retention
        DATEDIFF(client_session.created_at, user.installed_at) as delta_day
    FROM client_session LEFT JOIN user 
        ON (client_session.user_id = user.user_id)
    WHERE user.installed_at >= '2020-01-01'
        AND delta_day in (1, 3, 7)
    GROUP BY user.installed_at, delta_day) retention_table
LEFT JOIN
    (SELECT user.installed_at as installed_at,
        COUNT (DISTINCT user.user_id) as count_unique_user_install
    FROM client_session LEFT JOIN user 
        ON (client_session.user_id = user.user_id)
    WHERE user.installed_at >= '2020-01-01'
    GROUP BY user.installed_at) installed_table
ON retention_table.installed_at = installed_table.installed_at
GROUP BY installed_month
ORDER BY installed_month