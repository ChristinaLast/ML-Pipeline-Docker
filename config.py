def cat_config():
    ''' Configuration settings for columns in the datasets'''
    CAT_COLS = ['Property_Type','Listing_Type','Neighborhood']
    return CAT_COLS

def y_config(y_col_null_num, y_col_null_name):
    '''Configuration settings for y col'''
    Y_COL_NULL_NAME = 'Log_Revenue_(Native)'
    Y_COL_NULL_NUM = 21
    if y_col_null_num==True:
        return Y_COL_NULL_NUM
    if y_col_null_name==True:
        return Y_COL_NULL_NAME

def x_config(x_col_null_num, x_col_null_name):
    '''Configuration settings for x col'''
    X_COL_NULL_NUM = 1
    X_COL_NULL_NAME = 'Occupancy_Rate'
    if x_col_null_num==True:
        return X_COL_NULL_NUM
    if x_col_null_name==True:
        return X_COL_NULL_NAME

def crs_config():
    '''Configuration settings for coordinate reference system'''
    crs={'init': 'epsg:4326'}
    return crs

def model_config(model_1):
    MODEL_1_COL_NAME = ['Bedrooms','Occupancy_Rate','Number_of_Reservations','Log_Revenue_(Native)']
    
    if model_1==True:
        return MODEL_1_COL_NAME