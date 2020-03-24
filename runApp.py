from dataCleaning import load_data, clean_data, removing_outliers, normalize, log, aggregate_df, convert_yearly_income_2018_2019, one_hot_encoder, create_y, create_boxplot, classify_y, create_gdf, create_classification_col
import mapclassify as mc 

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

#aggregating by 'Property_ID' and averaging by year
Manchester_aggregated_df = aggregate_df(Manchester_no_outlier)
Oxford_aggregated_df = aggregate_df(Oxford_no_outlier)

#Convert the dataset that is in the form of monthly incomes to one which is yearly, and only keep data between 2018 and 2019
Manchester_df_yearly_merge = convert_yearly_income_2018_2019(Manchester_no_outlier)
Oxford_df_yearly_merge = convert_yearly_income_2018_2019(Oxford_no_outlier)

#one-hot encoding categorical columns
Manchester_ohe = one_hot_encoder(Manchester_log_norm)
Oxford_ohe = one_hot_encoder(Oxford_log_norm)

# creating gdf to store location information
Manchester_gdf = create_gdf(Manchester_ohe)
Oxford_gdf = create_gdf(Oxford_ohe)

# creating y variable for the classification
Manchester_y = create_y(Manchester_ohe)
Oxford_y = create_y(Oxford_ohe)

#creating boxplot based on 
Manchester_bp = create_boxplot(Manchester_y)
Oxford_bp = create_boxplot(Oxford_y)

#classifying y using different techniques
Manchester_fits = classify_y(Manchester_y)
Oxford_fits = classify_y(Oxford_y)

#creating gdf to store the 
Manchester_classified = create_classification_col(Manchester_gdf, Manchester_bp)
