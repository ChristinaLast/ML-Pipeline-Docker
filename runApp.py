from dataCleaning import load_data, clean_data, removing_outliers, normalize, log

# loading in data
Airbnb_Manchester = load_data('./app/data/Airbnb_Manchester.csv')
Airbnb_Oxford = load_data('./app/data/Airbnb_Oxford.csv')

# cleaning the NaN's from the data
Manchester_nona = clean_data(Airbnb_Manchester)
Oxford_nona = clean_data(Airbnb_Oxford)

# removing outliers from the dataset
Manchester_no_outlier = removing_outliers(Manchester_nona)
Oxford_no_outlier = removing_outliers(Oxford_nona)

#normalise y column
Manchester_y_norm = normalize(Manchester_no_outlier['Revenue_(Native)'])
Oxford_y_norm = normalize(Oxford_no_outlier['Revenue_(Native)'])

#log transforming normalised y column
Manchester_log_norm = log(Manchester_no_outlier, Manchester_y_norm)
Oxford_log_norm = log(Oxford_no_outlier, Oxford_y_norm)
