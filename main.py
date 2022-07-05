#import db.dbinsert as dbinsert
#import helper.logger as logger
#from helper.scraper import get_update_df
import pandas as pd
from datetime import datetime, timedelta, timezone
import pytz
#logger = logger.get_logger(__name__)

'''
p58b = nyiso("p58b", "http://mis.nyiso.com/public/csv/pal/", "pal.csv", "pal_csv.zip")
p58c = nyiso("p58c", "http://mis.nyiso.com/public/csv/palIntegrated/",
             "palIntegrated.csv", "palIntegrated_csv.zip")
p7 = nyiso("p7", "http://mis.nyiso.com/public/csv/isolf/", "isolf.csv", "isolf_csv.zip")
'''


table_metadata = {"p58b": ("http://mis.nyiso.com/public/csv/pal/", "pal.csv", "pal_csv.zip"),
               "p58c": ("http://mis.nyiso.com/public/csv/palIntegrated/", "palIntegrated.csv", "palIntegrated_csv.zip"),
               "p7" : ("http://mis.nyiso.com/public/csv/isolf/", "isolf.csv", "isolf_csv.zip")}

def get_current_date():
    return datetime.now(pytz.timezone('US/Eastern'))

def format_dt(curr_date):
    """
    Format datetime
    """
    formatted_dt = curr_date.strftime("%m-%d-%Y")
    dt_components = formatted_dt.split("-")
    return dt_components[2] + dt_components[0] + dt_components[1]

def format_dt_csv(curr_date):
    return curr_date.strftime("%m/%d/%Y %H:%M:%S")
    
def update(table_name):
    
    global table_metadata
    
    """
        Basic update functions
    """
    root_url = table_metadata[table_name][0]
    end_url = table_metadata[table_name][1]
    #zip_end_url = table_metadata[table_name][2]
    '''
    #updated to include changes to nyiso class with respect to updating df 5 minute intervals
    output = get_update_df(table_name, root_url, end_url)
    for time in output.keys():
        print("Inserting into database at time ", time, flush=True)
        dbinsert.insert_df(output[time], table_name, time)
    '''
    root_url = table_metadata[table_name][0]
    
    current_time = get_current_date()
    eastern = pytz.timezone('US/Eastern')
    
    if bool(datetime.now(eastern).dst()):
        current_time = current_time + timedelta(minutes=65)
    else:
        current_time = current_time + timedelta(minutes=5)

    

    url = root_url + format_dt(current_time) + end_url
    csv_dt = format_dt_csv(current_time)
    print("Making request to %s for data at %s", url, csv_dt)
    df = pd.read_csv(url)
    print(df)
    return df
    
def main():
    table_name = "p58b"
    update(table_name)
        
if __name__ == "__main__":
    main()
