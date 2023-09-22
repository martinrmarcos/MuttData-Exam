import argparse
## import some various libraries
##!pip install unidecode
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import re
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import unidecode
import urllib.request
import warnings
warnings.filterwarnings("ignore")
import argparse
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import time

from multiprocessing import Pool, cpu_count



logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


current_directory = os.getcwd()


main_path = current_directory+'/'


def fetch_data(date, coin):
    url = 'https://api.coingecko.com/api/v3/coins/'+coin+'/history?date='+date

    try:
        jsondump = urllib.request.urlopen(url).read()
        contents = json.loads(jsondump)
        market_data_json = contents['market_data']       
        newdata = pd.json_normalize(market_data_json)
        newdata.index = pd.to_datetime([date], format="%d-%m-%Y")
        newdata['json_data'] = [json.dumps(contents)]
        newdata['coin_id'] = coin
        time.sleep(wait_time)
        return newdata
    except:
        return None


def main():

    ### SQL data:
    username = 'postgres'
    password = 'Mutt2023'
    host = '0.0.0.0'  
    port = '5432'  
    database_name = 'MuttDB'
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database_name}')

    ### waiting time for API retrieval
    wait_time = 5

    ### Creation of a parser in order to be able to get the first 2 arguments after the file name
    ### in this case its going to be the coin desired and the date
    
    today_date = datetime.now().date()
    today_date = today_date.strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(   prog = 'GetCoinInfoForDay',
                                        description = "Gets all information for a specific coin and date")
    parser.add_argument("coin", type=str, help="the coin required")
    ### if there is not a second argument entered, it will asuume is for the same day download
    parser.add_argument("date", nargs='?', default=today_date, type=str, help="the date required")
    ### if a second date is entered it will create a bulk download
    parser.add_argument("to_date", nargs='?', default=None, type=str, help="the date required")
    ### if a fourth argument is entered it will save the data into postgresSQL
    parser.add_argument("save", nargs='?', default=None, type=str, help="y")
    args = parser.parse_args()

    if args.to_date is None:
        to_date = args.date
    else:
        to_date = args.to_date

    coin = args.coin
    date = args.date




    ### Creating a list of dates in order to be able to prcess them as bulk or as a single day
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
    except:
        print('wrong date structure entered')
        return



    date_list = []

    datedelta = date

    while datedelta <= to_date:
        date_list.append(datedelta.strftime("%d-%m-%Y"))
        datedelta += timedelta(days=1)

    date = date.strftime("%d-%m-%Y")
    to_date = to_date.strftime("%d-%m-%Y")

    logging.info('user entered '+date+' as a date')
    logging.info('user entered '+to_date+' as a to_date')
    logging.info('user entered '+coin+' as selected coin')



    path_to_save = main_path+'GetCoinInfoForDay_Results/GetCoinInfoForDay_'+coin+'_'+date+'_to_'+to_date+'.csv'

    # ### we save the desired URL to use and the desired values to extract

    # #dfs = {}
    # dfs = pd.DataFrame({})

    # ### For that iterates every date on the list created
    # for datediff in date_list:

    #     url = 'https://api.coingecko.com/api/v3/coins/'+coin+'/history?date='+datediff

    #     ### try added to handle bad connections
    #     try:
    #         jsondump = urllib.request.urlopen(url).read()
    #         contents = json.loads(jsondump)
    #         market_data_json = contents['market_data']       
    #         newdata = pd.json_normalize(market_data_json)
    #         newdata.index = pd.to_datetime([datediff], format="%d-%m-%Y")
    #         ### Saving the complete Json
    #         newdata['json_data'] = [json.dumps(contents)]
    #         #newdata['json_data'] = [json.dumps(contents)]
    #         newdata['coin_id'] = coin

    #         dfs = dfs.append(newdata)
    #         ### Waiting time was added as i was getting errors in the connection

    #         print(f"Waiting for {wait_time} seconds to be able to handle traffic")
    #         time.sleep(wait_time)
            
    #         logging.info('information has been loaded to a DataFrame for '+coin+' for the date: '+datediff)

    #     except:
    #         print(datediff+' for '+coin+' could not be loaded due to the APIs traffic restrictions')
    #         print(f"Waiting for {wait_time} seconds to be able to handle traffic")
    #         time.sleep(wait_time)

    def process_date_parallel(date):
        data = fetch_data(date, coin)
        if data is not None:
            logging.info('information has been loaded to a DataFrame for ' + coin + ' for the date: ' + date)
            return data
        else:
            logging.warning(date + ' for ' + coin + ' could not be loaded due to the APIs traffic restrictions')
            return None

    # Use multiprocessing to fetch data for multiple dates in parallel
    with Pool(processes=cpu_count()) as pool:
        dfs_list = pool.map(process_date_parallel, date_list)

    # Combine the results into a single DataFrame
    dfs = pd.concat([df for df in dfs_list if df is not None], ignore_index=True)





    #### Adding new functionality to save data into SQL

    if args.save is not None:

        logging.info('Opening SQL connection')

        connection = engine.connect()
        print('Connected to '+database_name+' database at '+host+':'+port)

        ### Getting the information requested for the first table in SQL

        table1_name = 'coin_price_usd'

        try:
            dftable1 = dfs[['coin_id', 'current_price.usd', 'json_data']]
            dftable1 = dftable1.reset_index()
            dftable1.rename(columns={'index': 'date'}, inplace=True)
        except:
            sql_query = 'SELECT * FROM '

            

            dfsqltable1 = pd.read_sql_query(sql_query+table1_name, engine)
            dftable1 = dfsqltable1


        ### Getting the already uploaded data to compare
        sql_query = 'SELECT * FROM '

        logging.info('Running: "'+sql_query+table1_name+' over the DB')
        dfsqltable1 = pd.read_sql_query(sql_query+table1_name, engine)

        ### Getting both dfs together to analyse the data
        dftable1 = dftable1.append(dfsqltable1)

        ### Getting the highest value per date in order to upload to SQL
        #dftable1 = dftable1.groupby('date').max().reset_index()
        #print(dftable1)
        dftable1 = dftable1.groupby(['date', 'coin_id', 'json_data']).max().reset_index()
        ### uploading the resulting df to SQL
        dftable1.to_sql(table1_name, engine, if_exists='replace', index=False)
        logging.info('Adding table nr 1 to the DB')



        ### preparing the second table to be uploaded, starting from the previous one

        table2_name = 'maxmin_monthly_usd'

        try:
            dftable2 = dfs[['coin_id', 'current_price.usd', 'json_data']]
            dftable2 = dftable2.reset_index()
            dftable2.rename(columns={'index': 'date'}, inplace=True)
            dftable2['month'] = dftable2['date'].dt.month
            dftable2['year'] = dftable2['date'].dt.year

            ### getting the max and min values per month after grouping it
            agg_functions = {'current_price.usd': ['max', 'min']}
            dftable2 = dftable2.groupby(['year', 'month', 'coin_id']).agg(agg_functions).reset_index()
            dftable2.columns = ['year', 'month', 'coin_id', 'max_price', 'min_price']
        except:
            ### Getting the already uploaded data to compare

            dfsqltable2 = pd.read_sql_query(sql_query+table2_name, engine)
            dftable2 = dfsqltable2



        ### Getting the already uploaded data to compare

        logging.info('Running: "'+sql_query+table2_name+' over the DB')
        dfsqltable2 = pd.read_sql_query(sql_query+table2_name, engine)

        ### Getting both dfs together to analyse the data
        dftable2 = dftable2.append(dfsqltable2, ignore_index = True)

        ### getting the max max an min min values per datapoint
        agg_functions = {'max_price': 'max','min_price': 'min'}
        dftable2 = dftable2.groupby(['year', 'month', 'coin_id']).agg(agg_functions).reset_index()

        ### uploading the resulting df to SQL
        dftable2.to_sql(table2_name, engine, if_exists='replace', index=False)
        logging.info('Adding table nr 2 to the DB')

        # Close the connection when done
        connection.close()
        logging.info('Clossing SQL connection')

        #return 0

    ### Saving a new DF as a CSV, with the date as index and all the information i columns
    print('DF was saved at: '+path_to_save)
    print('Great Success!!!')
    return pd.DataFrame(dfs).to_csv(path_to_save)



if __name__ == "__main__":
    main()















