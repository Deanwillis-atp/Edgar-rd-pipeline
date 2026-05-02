'Ranking the first 10 companies on spike percent in descending order'
mysql> WITH rank_growth AS 
    -> (SELECT spike_percentage,company_name, 
    -> RANK() OVER(ORDER BY spike_percentage  DESC) as rnk 
    -> FROM rd_spikes_flat) SELECT * FROM rank_growth WHERE rnk <=10;
'NOTICE -> "spike_percentage" is defined by the percentage increase of the most spent on R&D over the average of the other quarters. e.g( other_quarters =[ 10_000, 8_000], avg = 9,000 spike = 30,000 spike_percentage = 233.33% )'
+-------------------+------------------------------------+-----+
| spike_percentage | company_name                        | rnk |
+-------------------+------------------------------------+-----+
|            299900 | NOVA LIFESTYLE, INC.               |   1 |
|            201687 | APOLLO SOLAR ENERGY, INC.          |   2 |
|            102742 | DYADIC INTERNATIONAL INC           |   3 |
|           91543.8 | DYADIC INTERNATIONAL INC           |   4 |
|           50965.4 | NUGENEREX IMMUNO-ONCOLOGY, INC.    |   5 |
|             30380 | PERNIX THERAPEUTICS HOLDINGS, INC. |   6 |
|           25911.5 | CORONADO BIOSCIENCES INC           |   7 |
|           25911.5 | CORONADO BIOSCIENCES INC           |   7 |
|           25233.5 | AXIOM CORP.                        |   9 |
|           23115.4 | ALPHA-EN CORP                      |  10 |
+-------------------+------------------------------------+-----+
10 rows in set (0.016 sec)
'NOTICE -> Company 8 is skipped'

mysql> mysql> WITH rank_growth AS (SELECT spike_percentage,company_name,DENSE_RANK() OVER(ORDER BY spike_percentage  DESC) as rnk FROM rd_spikes_flat) SELECT * FROM rank_growth WHERE rnk <=10
    -> ;
+-------------------+------------------------------------+-----+
| spike_percentage | company_name                        | rnk |
+-------------------+------------------------------------+-----+
|            299900 | NOVA LIFESTYLE, INC.               |   1 |
|            201687 | APOLLO SOLAR ENERGY, INC.          |   2 |
|            102742 | DYADIC INTERNATIONAL INC           |   3 |
|           91543.8 | DYADIC INTERNATIONAL INC           |   4 |
|           50965.4 | NUGENEREX IMMUNO-ONCOLOGY, INC.    |   5 |
|             30380 | PERNIX THERAPEUTICS HOLDINGS, INC. |   6 |
|           25911.5 | CORONADO BIOSCIENCES INC           |   7 |
|           25911.5 | CORONADO BIOSCIENCES INC           |   7 |
|           25233.5 | AXIOM CORP.                        |   8 |
|           23115.4 | ALPHA-EN CORP                      |   9 |
|           19946.9 | APPTIGO INTERNATIONAL, INC.        |  10 |
|           19946.9 | INNOVATION ECONOMY CORP            |  10 |
|           19946.9 | INNOVATION ECONOMY CORP            |  10 |
+-------------------+------------------------------------+-----+
13 rows in set (0.013 sec)
'NOTICE -> Includes position 8'
'Sorting all companies average spike percentage into 4 buckets.'
'Shows that the top 25% of companies have the largest spikes in R&D spending.'
mysql> WITH bucket AS
    -> ( SELECT spike_percentage,
    -> NTILE(4) OVER (ORDER BY spike_percentage DESC) AS buk 
    -> FROM rd_spikes_flat) SELECT buk AS quarter, AVG( spike_percentage) 
    -> AS growth FROM bucket GROUP BY buk;
+---------+--------------------+
| quarter | growth             |
+---------+--------------------+
|       1 |  810.9178159270967 |
|       2 |   35.6839196400983 |
|       3 | 15.634184898676326 |
|       4 |  5.654604728947185 |
+---------+--------------------+
4 rows in set (0.013 sec)
'Compairing the spike percentage to the prior filling dates spike percentage'
mysql> SELECT company_name, report_date, spike_percentage, 
    -> LAG(spike_percentage) OVER(PARTITION BY company_name ORDER BY report_date ASC)previous_growth , 
    -> LAG(report_date) OVER(PARTITION BY company_name ORDER BY report_date ASC)  AS previous_growth_date  
    -> FROM rd_spikes_flat LIMIT 5;
+--------------------------+-------------+-------------------+-----------------+----------------------+
| company_name             | report_date | spike_percentage  | previous_growth | previous_growth_date |
+--------------------------+-------------+-------------------+-----------------+----------------------+
| 2050 MOTORS, INC.        | 2016-03-31  |            302.71 |            NULL | NULL                 |
| 22ND CENTURY GROUP, INC. | 2013-03-31  |             23.86 |            NULL | NULL                 |
| 22ND CENTURY GROUP, INC. | 2014-09-30  |             43.84 |           23.86 | 2013-03-31           |
| 22ND CENTURY GROUP, INC. | 2022-06-30  |             54.29 |           43.84 | 2014-09-30           |
| 22ND CENTURY GROUP, INC. | 2023-06-30  |             14.57 |           54.29 | 2022-06-30           |
+--------------------------+-------------+-------------------+-----------------+----------------------+
5 rows in set (0.044 sec)
'Finding the running average of spike percentage per company'
mysql> SELECT company_name,report_date,spike_percentage, AVG(spike_percentage) 
    -> OVER(PARTITION BY company_name ORDER BY report_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW ) 
    -> as running_avg FROM rd_spikes_flat LIMIT 10;
+--------------------------+-------------+-------------------+--------------------+
| company_name             | report_date | spike_percentage  | running_avg        |
+--------------------------+-------------+-------------------+--------------------+
| 2050 MOTORS, INC.        | 2016-03-31  |            302.71 |  302.7099914550781 |
| 22ND CENTURY GROUP, INC. | 2013-03-31  |             23.86 | 23.860000610351562 |
| 22ND CENTURY GROUP, INC. | 2014-09-30  |             43.84 |  33.85000038146973 |
| 22ND CENTURY GROUP, INC. | 2022-06-30  |             54.29 | 40.663333892822266 |
| 22ND CENTURY GROUP, INC. | 2023-06-30  |             14.57 | 34.140000343322754 |
| 2SEVENTY BIO, INC.       | 2020-09-30  |             53.87 | 53.869998931884766 |
| 2SEVENTY BIO, INC.       | 2021-03-31  |             24.29 | 39.079999923706055 |
| 3D SYSTEMS CORP          | 2015-06-30  |             15.18 | 15.180000305175781 |
| 3D SYSTEMS CORP          | 2016-09-30  |             26.88 |  21.02999973297119 |
| 3D SYSTEMS CORP          | 2019-03-31  |              4.92 |  15.65999984741211 |
+--------------------------+-------------+-------------------+--------------------+
10 rows in set (0.018 sec)
'Finding the max spike percentage per company'
mysql> WITH rank_table AS (SELECT company_name,report_date,spike_percentage , DENSE_RANK() OVER(PARTITION BY company_name ORDER BY spike_percentage DESC) as rnk FROM rd_spikes_flat) SELECT company_name,report_date,spike_percentage FROM rank_table WHERE rnk <=1 LIMIT 5;
+--------------------------+-------------+-------------------+
| company_name             | report_date | spike_percentage  |
+--------------------------+-------------+-------------------+
| 2050 MOTORS, INC.        | 2016-03-31  |            302.71 |
| 22ND CENTURY GROUP, INC. | 2022-06-30  |             54.29 |
| 2SEVENTY BIO, INC.       | 2020-09-30  |             53.87 |
| 3D SYSTEMS CORP          | 2016-09-30  |             26.88 |
| 3D TOTAL SOLUTIONS INC.  | 2014-03-31  |            417.15 |
+--------------------------+-------------+-------------------+
5 rows in set (0.027 sec)




