import pandas as pd
import numpy as np
from scipy import stats
import geopandas as gpd
import config
import mapclassify as mc

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

def aggregate_df(df_merge):
    print("Aggregate the data by Property ID and creating a table of yearly averages")
    aggregated_df = df_merge.groupby('Property_ID')[["Revenue_(Native)", "Occupancy_Rate", "Number_of_Reservations"]].mean().rename(columns={'Revenue_(Native)' : 'Yearly_Revenue',
                     'Occupancy_Rate' : 'Yearly_Occupancy_Rate',
                     'Number_of_Reservations': 'Average_Yearly_Reservations'}).reset_index()
    print("First 5 rows of the dataframe: ",aggregated_df.head())
    
    return aggregated_df

def convert_yearly_income_2018_2019(df_merge):
    #Create Year column from 'Reporting_Month'
    df_merge['Year'] = df_merge.Reporting_Month.dt.year
    print('Created "Year" column from "Reporting_Month""')
    
    # Groupby Property ID and Year
    df_grouped =  df_merge.groupby(['Property_ID','Year']).mean().reset_index()
    #  Filter data by 2018 and 2019 
    df_filtered = df_grouped.loc[df_grouped['Year'].isin(['2018','2019'])]
    print('Groupby "Property_ID" and "Year" and filtered data for 2018 and 2019')

    # merging all other columns and dropping Reporting_Month as no longer relevant
    df_yearly_merge = pd.merge(df_filtered, df_merge).drop('Reporting_Month', axis=1)

    # printing the first 5 rows of the dataframe
    print("First 5 rows of the dataframe: ",df_yearly_merge.head())
    
    return df_yearly_merge

def one_hot_encoder(df_merge):
    '''
    This function gets category columns specified in the config file and 
    creates new columns with the following format: `<column__value>`.
    ''' 
    df_ohe = pd.get_dummies(df_merge, prefix_sep="__", columns = config.cat_config())
    
    return df_ohe

def create_y(df_ohe):
    # retrieving column containing y variable from the config file. 
    y = df_ohe[config.y_config(y_col_name=True, y_col_num=False)]
    
    return y

def classify_y(y):
    # generating classification objects from the data
    q5 = mc.Quantiles(y, k=5)
    ei5 = mc.EqualInterval(y, k=5)
    mb5 = mc.MaximumBreaks(y, k=5)
    fits = [c.adcm for c in [q5, ei5, mb5]]
    print('Fits: ', fits)
    return fits

def create_gdf(df_ohe):
    col_geometry = gpd.GeoDataFrame(df_ohe, geometry=gpd.points_from_xy(df_ohe.Longitude, df_ohe.Latitude))
    gdf = gpd.GeoDataFrame(col_geometry, crs=config.crs_config(), geometry='geometry')
    return gdf

def create_boxplot(y):
    bp = mc.BoxPlot(y)
    # printing output of boxplot
    print(bp)
    return bp

def create_classification_col(gdf, bp):
    # generating labels for boxplot classification of y variable
    labels = ['0-low outlier', '1-low whisker',
          '2-Q2', '3-Q3', '4-high whisker', '5-high outlier']
    bpl = [ labels[b] for b in bp.yb ]
    bp_array = np.asarray(bpl)
    gdf["Box_Plot_Labels"] = bp_array
    # printing the first five rows of the geodataframe
    print("First 5 rows of the geodataframe: ",gdf.head())
    
    return gdf

def create_xy_dataframe(df_ohe, model_null, model_1, x_col_null_name, x_col_null_num, x_col_1_name, x_col_1_num, y_col_name, y_col_num):
    #selecting the columns based on the config file
    if config.model_config(model_null==True, model_1==False):
        df_xy_null = df_ohe[[config.y_config(y_col_name=True, y_col_num=False),config.x_config(x_col_null_name=True, x_col_null_num=False, x_col_1_num=False, x_col_1_name=False)]]
        return df_xy_null
    
    if config.model_config(model_1==True, model_null==False):
        df_xy_1 = df_ohe[[config.y_config(y_col_name=True, y_col_num=False),config.x_config(x_col_null_name=False, x_col_null_num=False, x_col_1_name=True, x_col_1_num=False)]]
        return df_xy_1
