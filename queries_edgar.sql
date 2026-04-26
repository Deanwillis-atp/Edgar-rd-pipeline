mysql> show databases;
+-----------------------+
| Database              |
+-----------------------+
| aggregated_stock_data |
| fintech               |
| information_schema    |
| mysql                 |
| performance_schema    |
| sys                   |
| test                  |
+-----------------------+
7 rows in set (0.002 sec)

mysql> use aggregated_stock_data;
Database changed
mysql> show tables;
Empty set (0.003 sec)

mysql> show tables;
+---------------------------------+
| Tables_in_aggregated_stock_data |
+---------------------------------+
| financial_data                  |
| metadata                        |
+---------------------------------+
2 rows in set (0.003 sec)

mysql> select count(*) from financial_data;
+----------+
| count(*) |
+----------+
|  1060049 |
+----------+
1 row in set (0.037 sec)

mysql> select count(*) from metadata;
+----------+
| count(*) |
+----------+
|   189541 |
+----------+
1 row in set (0.013 sec)

mysql> select * from metadata limit 5;
+----------------------+------+--------------------------------+------------+------+
| adsh                 | cik  | name                           | filed      | form |
+----------------------+------+--------------------------------+------------+------+
| 0000002178-14-000044 | 2178 | ADAMS RESOURCES & ENERGY, INC. | 2014-05-12 | 10-Q |
| 0000002178-14-000056 | 2178 | ADAMS RESOURCES & ENERGY, INC. | 2014-08-11 | 10-Q |
| 0000002178-14-000064 | 2178 | ADAMS RESOURCES & ENERGY, INC. | 2014-11-07 | 10-Q |
| 0000002178-15-000030 | 2178 | ADAMS RESOURCES & ENERGY, INC. | 2015-05-08 | 10-Q |
| 0000002178-15-000040 | 2178 | ADAMS RESOURCES & ENERGY, INC. | 2015-08-07 | 10-Q |
+----------------------+------+--------------------------------+------------+------+
5 rows in set (0.000 sec)

mysql> SELECT metadata.cik, metadata.name,metadata.filed, financial_data.tag,financial_data.ddate,financial_data.value FROM financial_data JOIN metadata ON financial_data.adsh = metadata.adsh WHERE financial_data.tag = 'ResearchAndDevelopmentExpense' ORDER BY metadata.cik ,financial_data.ddate;
+---------+---------------------------------------------------+------------+-------------------------------+------------+----------------+
| cik     | name                                              | filed      | tag                           | ddate      | value          |
+---------+---------------------------------------------------+------------+-------------------------------+------------+----------------+
|    1800 | ABBOTT LABORATORIES                               | 2019-05-01 | ResearchAndDevelopmentExpense | 2018-03-31 |   589000000.00 |
|    1800 | ABBOTT LABORATORIES                              
'continues...'

mysql> CREATE TABLE company_financials AS SELECT metadata.cik, metadata.name,metadata.filed, financial_data.tag,financial_data.ddate,financial_data.value, financial_data.qtrs FROM financial_data JOIN metadata ON financial_data.adsh = metadata.adsh WHERE financial_data.tag = 'ResearchAndDevelopmentExpense' AND financial_data.qtrs = 1 AND financial_data.value IS NOT NULL ORDER BY metadata.cik ,financial_data.ddate;
Query OK, 108310 rows affected (2.541 sec)
Records: 108310  Duplicates: 0  Warnings: 0

mysql> show tables;
+---------------------------------+
| Tables_in_aggregated_stock_data |
+---------------------------------+
| company_financials              |
| financial_data                  |
| metadata                        |
+---------------------------------+
3 rows in set (0.003 sec)
