import requests,time,os,zipfile
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


headers = {'User-Agent': 'Dean Deanwillis@outlook.com'} #{'User_Agent':'first_name email address'} required to download from government
base_url ='https://www.sec.gov/files/dera/data/financial-statement-data-sets-archive/' #where data is downloaded from
download_folder = "/Users/dean/Desktop/Projects_github/edgar_bulk/" #where data will go on your computer
unzipped_download_folder = "/Users/dean/Desktop/Projects_github/edgar_bulk_unzipped/" 
extracted_files = ['num.txt','sub.txt'] # what files will be extracted
name_of_first_file = ['download_2014q1.zip'] #the first file name 
first_date = ['2014q1'] #the first date you want to extract increases by 1 year includes all 4 quarters

#extracting files from web
def dates():
    dates_url = first_date
    date = 2014 #starting date
    quarter = 'q'
    quarter_num = 1 #starting quarter
    for i in range(39):
        quarter_num += 1
        if quarter_num == 5:
            quarter_num = 1
            date +=1
        x = str(date) + quarter + str(quarter_num)
        dates_url.append(x)
    return dates_url

dates = dates() #passed as 'moving_dates'


def download_batch(moving_dates):
    file_path = download_folder
    os.makedirs(file_path, exist_ok=True)
    for i in moving_dates:
        file_name = 'download_' + i + '.zip' #creating file names using dates function
        url = (base_url +i+'-archive.zip')
        full_path = os.path.join(file_path,file_name)
        print(f'downloading:  {file_name} to:  {file_path}')
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            with open (full_path,'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f'downloaded {file_name}')
        else:
            print(f"error code: {response.status_code}")
        
        time.sleep(0.5) # to not be flagged by government

download_batch(dates)


    
def get_full_file_name(moving_dates): #might be redundant 
    fle_name = name_of_first_file
    for i in moving_dates: 
        x = 'download_' + i + '.zip'
        fle_name.append(x) 
    return fle_name



#unzipping and extracting files from already downloaded files
def extract_data(files):
    file_path = download_folder
    new_file_path = unzipped_download_folder
    files_to_extract = extracted_files
    for i in files: 
        full_path = os.path.join(file_path,i)

        with zipfile.ZipFile(full_path,'r') as unzip:
            for file_ in files_to_extract:
                try:
                    unzip.extract(file_, path=new_file_path)
                    old_name = os.path.join(new_file_path, file_)
                    new_name = os.path.join(new_file_path, f"{i[:-4]}_{file_}")
                    os.rename(old_name, new_name)
                    print(f"unzipped {i}")
                except KeyError:
                    print(f'Error: {i} not found ')

file_name = get_full_file_name(dates)
extract_data(file_name)


# pushing data to sql, requires your own info and mySQL with database name already created


def send_to_sql():
    host='localhost'
    user='root' 
    password=''
    database='aggregated_stock_data'

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

    saved_tags = [
        'ResearchAndDevelopmentExpense',
        'NetIncomeLoss',
        'Revenues'
    ]

    for file_name in os.listdir(unzipped_download_folder):
        file_path = os.path.join(unzipped_download_folder,file_name)
        if 'num' in file_name:
            read = pd.read_csv(file_path, sep='\t' , dtype=str) #values are seperated by tabs not ','s
            filter_tags = read[read['tag'].isin(saved_tags)]
            filter_quarts = filter_tags[filter_tags['qtrs']=='1'] #only looking at the current quarter ('1') not the whole year ('4')
            selected_columns = filter_quarts[['adsh', 'tag', 'ddate', 'qtrs', 'value']] #keep these 
            selected_columns['value'] = pd.to_numeric(selected_columns['value'], errors='coerce')
            selected_columns['ddate'] = pd.to_datetime(selected_columns['ddate'], errors='coerce')
            selected_columns.to_sql('financial_data', con=engine, if_exists='append', index=False)
            print(f"pushed {file_name} to sql")

        elif 'sub' in file_name:
            read_sub = pd.read_csv(file_path,sep='\t', dtype=str)
            filter_quarterly = read_sub[read_sub['form'] =='10-Q']
            selected_columns_sub = filter_quarterly[['adsh', 'cik', 'name', 'filed', 'form']]
            selected_columns_sub['filed'] = pd.to_datetime(selected_columns_sub['filed'], errors='coerce')
            selected_columns_sub['cik'] = pd.to_numeric(selected_columns_sub['cik'], errors='coerce')
            selected_columns_sub.to_sql('metadata', con=engine, if_exists='append', index=False)
            print(f"pushed {file_name} to sql")
    print("uploaded to sql")

send_to_sql()