import pandas as pd
import numpy as np
from scipy import stats
import geopandas as gpd

#Loading data to dataframe, converting variables to strings and removing whitespace from columns
def load_data(path_to_csv):
    print("Loading Data")
    # Importing csv to dataframe and variables to string
    df = pd.read_csv(path_to_csv,
                converters={'Property ID': lambda x: str(x),
                            'Host ID': lambda x: str(x),
                            'Zipcode': lambda x: str(x),
                            'Neighborhood': lambda x: str(x),
                            'Metropolitan Statistical Area': lambda x: str(x)}).rename(columns=lambda x: x.replace(' ', '_'))
    
    # Converting column to datetime format (using infer_datetime_format to increase parsing speed)
    df['Reporting_Month'] = pd.to_datetime(df['Reporting_Month'],infer_datetime_format=True)

    return df

#cleaning data and filtering out NaN results
def clean_data(df):
    print("Cleaning Data")
    #susetting columns which contain ancillary information to the task or repeat information
    # e.g. Revenue_(USD) and 'Revenue_(Native)'
    subset=['Scraped_During_Month', 'Currency_Native', 'Host_ID']
    
    # Dropping columns where all results are NA
    print("Original shape: ",df.shape)
    df.drop(subset, axis=1, inplace=True)
    print("Shape after dropping columns with all NA results: ",df.shape)
    
    # Dropping rows where results are NA
    df_filtered = df.dropna()
    print("Shape after dropping rows with NA results: ",df_filtered.shape)

    return df_filtered

# removing extreme outliers from the data
def removing_outliers(df_filtered):
    print("Removing outliers")
    print("Shape after dropping columns with all NA results: ",df_filtered.shape)
    df_num = df_filtered.select_dtypes(['number'])
    print("Shape after dropping nonumeric columns: ",df_num.shape)

    # Setting the threshold for acceptable z-scores as 3
    z = np.abs(stats.zscore(df_num))
    
    df_no_outliers = df_num[(z < 3).all(axis=1)]
    print("Shape after dropping rows where z score exceeds threshold: ", df_no_outliers.shape)
    
    # append result back to clean dataframe
    df_merge = pd.merge(df_no_outliers, df_filtered)
    print("Shape after concatenating dataframe: ", df_merge.shape)
    
    return df_merge

def normalize(y_col):
    print("Normalizing y variable")
    upper = y_col.max()
    lower = y_col.min()
    y = (y_col - lower)/(upper-lower)
    return y

#log the y variable if non-normally distributed
def log(df_merge, y):
    print("Log transforming y variable")
    #log the non-normally distributed columns and assign to new column in the dataframe
    y_log = np.log(y + 1)
    # normalize the log series
    y_log_norm = normalize(y_log)
    print("Descriptive statistics of the log transformed result:", y_log_norm.describe())
    # convert series object into a dataframe 
    df_merge['Log_Revenue_(Native)'] = y_log_norm
    
    return df_merge
