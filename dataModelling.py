import config 

def train_test_split(df_xy):
    ''' This function splits the dataframe into a training and test dataset with 
    80% of the data in the training dataset '''
    train_df = df_xy.sample(frac=0.8,random_state=0)
    test_df = df_xy.drop(train_df.index)
    
    return train_df, test_df

def x_data_description(train_df):
    train_df_x_stats = train_df.describe()
    # removing the y variable from the dataframe using the config file
    train_df_y = train_df_x_stats.pop(config.x_config(x_col_null_num=False, x_col_null_name=True))
    # transposing the results to have the descriptive statistics as columns
    train_df_x_stats = train_df_x_stats.transpose()

    print("X variable description: ",train_df_x_stats)

    return train_df_y, train_df_x_stats

def y_data_description(train_df_y):
    train_df_y_stats = train_df_y.describe()

    # transposing the results to have the descriptive statistics as columns
    train_df_y_stats = train_df_y_stats.transpose()

    print("Y variable description: ",train_df_y_stats)

    return train_df_y_stats

