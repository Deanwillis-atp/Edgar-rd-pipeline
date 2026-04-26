import json,time
import yfinance as yf
from datetime import date, timedelta

# data = {
#     'QDEL': {'2022': [['2022-09-30', 65600000.0, 116.5]]}, 
#     'QBTS': {'2023': [['2023-03-31', 10915000.0, 14.85]]},
#     'ABT': {'2022': [['2022-09-30', 65600000.0, 116.5]]}}


def ticker_data_import():
    with open('ticker_data.json','r') as f:
        result = json.load(f)
    return result

result = ticker_data_import()
data = {k: v for k,v in result.items() if not str(k).isdigit()}


def find_price(dta):
    price_dict = {}
    for name in dta:
        ticker = yf.Ticker(name)
        for year in dta[name]:
            for info in dta[name][year]:
                
                date1 = info[0]
                date_of = date.fromisoformat(date1)
                #print(ticker,date_of)

                date_30_before_start = date_of - timedelta(days=30)
                date_30_before_end = date_30_before_start + timedelta(days=5)

                date_30_after_start = date_of + timedelta(days=30)
                date_30_after_end = date_30_after_start + timedelta(days=5)

                price_date_before = ticker.history(start=date_30_before_start,end=date_30_before_end)
                price_date_after = ticker.history(start=date_30_after_start,end= date_30_after_end)
                time.sleep(0.15)
                if not price_date_before.empty and not price_date_after.empty:
                    price_bf = round(price_date_before['Close'].iloc[0],2)
                    price_af = round(price_date_after['Close'].iloc[0],2)
                    info.append(f'Price around {date_30_before_start} - {price_bf}')
                    info.append(f'Price around {date_30_after_start} - {price_af}')
                    price_dict[name] = info

                else:
                    print(f'{name} {date1} no price data')
                    continue

price_dict = find_price(data)

with open('price_data.json', 'w') as f:
    json.dump(price_dict, f, default=str, indent=4) 






#dont need to run all companies existed 180 days before spikes
# def find_iop(dta):
#     cleaned_data = {}
#     for name in dta:
#         date1 = dta[name][0]
#         ticker = yf.Ticker(name)
#         date_of = date.fromisoformat(date1)
#         did_company_exist_start = date_of - timedelta(days=180)
#         did_company_exist_end = date_of + timedelta(days=7)
#         check = ticker.history(start=did_company_exist_start,end=did_company_exist_end)
#         time.sleep(0.15)
#         if not check.empty:
#             cleaned_data[name] = dta[name]
#         else:
#             print(f'removed {name}')
#             continue
            
#     return cleaned_data




