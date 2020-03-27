def cat_config():
    ''' Configuration settings for columns in the datasets'''
    CAT_COLS = ['Property_Type','Listing_Type','Neighborhood']
    return CAT_COLS

def y_config(y_col_num, y_col_name):
    '''Configuration settings for y col'''
    Y_COL_NAME = 'Log_Revenue_(Native)'
    Y_COL_NUM = 21
    if y_col_num==True:
        return Y_COL_NUM
    if y_col_name==True:
        return Y_COL_NAME


def x_config(x_col_null_num, x_col_null_name, x_col_1_num, x_col_1_name, x_col_2_name):
    '''Configuration settings for x cols'''
    X_COL_NULL_NUM = 1
    X_COL_NULL_NAME = 'Occupancy_Rate'
    X_COL_1_NAME_1 = 'Bedrooms'
    X_COL_1_NAME_2 = 'Number_of_Reservations'
    X_COL_1_NUM = 1, 
    if x_col_null_num==True:
        return X_COL_NULL_NUM
    if x_col_null_name==True:
        return X_COL_NULL_NAME
    if x_col_1_num==True:
        return X_COL_1_NUM
    if x_col_1_name==True:
        return X_COL_1_NAME_1
    if x_col_2_name==True:
        return X_COL_1_NAME_2

def crs_config():
    '''Configuration settings for coordinate reference system'''
    crs={'init': 'epsg:4326'}
    return crs

def model_config(model_null, model_1):
    ''' configuration settings for each model run'''
    if model_null==True:
        return model_null
    if model_1==True:
        return model_1