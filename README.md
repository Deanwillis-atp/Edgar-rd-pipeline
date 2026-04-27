# R&D expense spikes predict short term price declines 

## Overview
R&D expense spikes predict short term price declines with 55-68% accuracy across 1404 public companies, scaling with spike magnitude.
1.82GB SEC EDGAR data, 101k companies, ETL from zip to MySQL to Python, yfinance enrichment.

## Definitions
1. A spike is identified when exactly one quarter's R&D expense exceeds the average of all three quarters for that year.
2. Spike percent is defined by the percentage increase in spending than normal(three quarters).
3. Spikes are sorted into buckets (10%, 10%-20%..etc)
4. Decreases are defined by stock prices that are taken 30 days before and after spike date.


## Data found 
<img width="1033" height="568" alt="Screenshot 2026-04-26 at 8 37 51 PM" src="https://github.com/user-attachments/assets/da20300c-f62d-457d-974e-b9e9bd48451c" />




## Limitations
1. Stock price only taken in a 30 day window may predate 10-k filings.
2. Only 3 quarters of data (quarter 4 not filed in 10-k).
3. Data taken only from 2014-2023 (not live data).
4. Data lost due to issues with ticker symbols.

I plan on making a version without any of the listed limitations


## Data Source
SEC EDGAR Financial Statement Data Sets (2014 Q1 - 2023 Q4)
https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets-archive

## Tools Used
- Python (zipfile, requests, sqlalchemy)
- MySQL
  

