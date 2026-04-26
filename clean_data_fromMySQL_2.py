import mysql.connector
from datetime import datetime
import json
from pytickersymbols import PyTickerSymbols
import requests,time

headers = {
    'User-Agent': 'MyCompany Dean Willis Deanwillis@outlook.com',
}
def bring_in_data():
    data = {}
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='aggregated_stock_data'
    )
    
    cursor = db_connection.cursor()
    query = 'SELECT DISTINCT cik,ddate,value FROM company_financials ;' #There was duplicate data
    cursor.execute(query)
    # values = []
    # quarters = []
    
    for cik,ddate,value in cursor:
        if cik not in data:
            data[cik] = {'info':[[ddate,value]]}
        elif cik in data:
            data[cik]['info'].append([ddate,value]) 
    return data

       
            
data = bring_in_data()





def group_by_year(dta):
    group_year_dict = {}
    for name in dta:
        for data in dta[name]['info']:
            

            year = data[0].year
            date = data[0]
            value = float(data[1])

            if name not in group_year_dict:
                group_year_dict[name] = {}

            if year not in group_year_dict[name]:
                group_year_dict[name][year] = []

            group_year_dict[name][year].append([date,value])

    return group_year_dict
            
group_year = group_by_year(data)
#print(group_year)

def avgp_prec(gryear):
    avg_price_precent = {}
    entries = 0
    for name in gryear:
        for year in gryear[name]:

            spiked_num = None
            spiked_date = None
            sum_rd = []
            amount = 0

            for info in gryear[name][year]: 

                sum_rd.append((info[0],float(info[1])))
            
            prices = [i[1]for i in sum_rd]
            
            for i in prices:
                
                if i > 1:
                    
                    if len(prices) >= 3:
                        entries+=1
                        
                        max_value = max(prices)
                        avg_of_sumrd = (sum(prices) / len(prices))

                        if avg_of_sumrd > 1:
            
                            avg_without_spiked = sum(p for p in prices if p != max_value) / (len(prices) - 1)
                            if avg_without_spiked > 1:
                                prec_inc = (((max_value)-(avg_without_spiked))/(avg_without_spiked)*100)
                            

            for i in sum_rd:
                if i[1] > avg_of_sumrd:
                    amount+=1
                    spiked_num = i[1]
                    spiked_date = i[0]
            
            if name not in avg_price_precent:
                avg_price_precent[name] = {}
            if amount == 1:
                
                avg_price_precent[name][year] = [[spiked_date,spiked_num,round(prec_inc, 2)]]
                        
    return    avg_price_precent #,entries


avg_price_and_precent1 = avgp_prec(group_year)
avg_price_and_precent = {name: years for name, years in avg_price_and_precent1.items() if years}
print(len(avg_price_and_precent))


#https://data.sec.gov/submissions/CIK0000001234.json

def find_ticker(dta):
    ticker_dict = {}
    for i in dta:
        cik = str(i)
        add_zeros = cik.zfill(10)
        
        url = f'https://data.sec.gov/submissions/CIK{add_zeros}.json'
        open_url = requests.get(url,headers=headers)
        print(open_url.status_code)
        time.sleep(0.15) 
        if open_url.status_code == 200:
            in_url = open_url.json()
            ticker = in_url.get('tickers')
            print(ticker)
            if ticker:
                tickers = ticker[0]
                ticker_dict[tickers] = dta[i]
            elif len(ticker) == 0:
                print(url)
                ticker_dict[cik] = dta[i]

        else:
            continue
    return ticker_dict


# result = find_ticker(avg_price_and_precent)

def store_dta(dta):
    with open('ticker_data.json', 'w') as f:
        json.dump(dta,f,default = str,indent=4)
    print('done')

# store_dta(result)

