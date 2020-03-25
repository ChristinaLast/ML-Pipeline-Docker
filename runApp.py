from dataCleaning import load_data, clean_data, removing_outliers, normalize, log, aggregate_df, convert_yearly_income_2018_2019, one_hot_encoder, create_y, create_boxplot, classify_y, create_gdf, create_classification_col, create_xy_dataframe
from dataModelling import train_test_split, x_data_description, y_data_description
import mapclassify as mc 
import config

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

#creating gdf to store the classification information
Manchester_classified = create_classification_col(Manchester_gdf, Manchester_bp)
Oxford_classified = create_classification_col(Oxford_gdf, Oxford_bp)

#Creating a dataframe with only the x and y for model 1 to Predict Airbnb Revenue
Manchester_Data_xy = create_xy_dataframe(Manchester_ohe) 
Oxford_Data_xy = create_xy_dataframe(Oxford_ohe)

#Creating a dataframe with only the x variable model 1 to Predict Airbnb Revenue
Manchester_Data_x = Manchester_ohe.iloc[:, [config.x_config(x_col_null_num=True, x_col_null_name=False)]]
Oxford_Data_x = Oxford_ohe.iloc[:, [config.x_config(x_col_null_num=True, x_col_null_name=False)]]

#Creating a dataframe with only the y variable for model 1 to Predict Airbnb Revenue
Manchester_Data_y = Manchester_ohe.iloc[:, [config.y_config(y_col_null_num=True, y_col_null_name=False)]]
Oxford_Data_y = Oxford_ohe.iloc[:, [config.y_config(y_col_null_num=True, y_col_null_name=False)]]

#creating test and train dataset from the new xy dataframe
Manchester_train_df_null, Manchester_test_df_null = train_test_split(Manchester_Data_xy)
Oxford_train_df_null, Oxford_test_df_null = train_test_split(Oxford_Data_xy)

#describing the x and y variables of the model
Manchester_train_df_x_stats = x_data_description(Manchester_train_df_null)
Oxford_train_df_x_stats = x_data_description(Oxford_train_df_null)

Manchester_train_df_y_stats = y_data_description(Manchester_train_df_null)
Oxford_train_df_y_stats = y_data_description(Oxford_train_df_null)

