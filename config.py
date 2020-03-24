def cat_config():
    ''' Configuration settings for columns in the datasets'''
    CAT_COLS = ['Property_Type','Listing_Type','Neighborhood']
    return CAT_COLS

def y_config():
    '''Configuration settings for y col'''
    Y_COL = 'Log_Revenue_(Native)'
    return Y_COL

def crs_config():
    '''Configuration settings for coordinate reference system'''
    crs={'init': 'epsg:4326'}
    return crs