import config 
#import tensorflow as tf
#from tensorflow import keras
#from tensorflow.keras import layers

def train_test_split(df_xy):
    ''' This function splits the dataframe into a training and test dataset with 
    80% of the data in the training dataset '''
    train_df = df_xy.sample(frac=0.8,random_state=0)
    test_df = df_xy.drop(train_df.index)
    
    return train_df, test_df

def x_data_description(train_df):
    train_df_x_stats = train_df.describe()
    # removing the y variable from the dataframe using the config file
    train_df_x_stats = train_df_x_stats.pop(config.x_config(x_col_null_num=False, x_col_null_name=True))
    # transposing the results to have the descriptive statistics as columns
    train_df_x_stats = train_df_x_stats.transpose()

    print("X variable description: ",train_df_x_stats)

    return train_df, train_df_x_stats

def y_data_description(train_df):
    train_df_y_stats = train_df.describe()

    # transposing the results to have the descriptive statistics as columns
    train_df_y_stats = train_df_y_stats.transpose()

    print("Y variable description: ",train_df_y_stats)

    return train_df_y_stats

def norm(train_df, train_df_x_stats):
    return (train_df - train_df_x_stats['mean']) / train_df_x_stats['std']

def build_model(train_df):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(train_df.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
    return model

def data_description(train_df, model_config, model_null, model_1):
    if config.model_config(model_null=True):
        
        # creating the data frame with the x variables in null model 
        Manchester_train_df_null = train_test_split(
            train_df[config.y_config(
                y_col_num=False, y_col_name=True),
            config.x_config(
                x_col_null_num=False, x_col_null_name=True)])
        Oxford_train_df_null = train_test_split(
            train_df[config.y_config(
                y_col_num=False, y_col_name=True),
            config.x_config(
                x_col_null_num=False, x_col_null_name=True)])

        #describing the x and y variables of the null model 
        Manchester_train_df_x_stats_null = x_data_description(Manchester_train_df_null)
        Oxford_train_df_x_stats_null = x_data_description(Oxford_train_df_null)
        
        Manchester_train_df_y_stats_null = y_data_description(Manchester_train_df_null)
        Oxford_train_df_y_stats_null = y_data_description(Oxford_train_df_null)

        return Manchester_train_df_null, Oxford_train_df_null, Manchester_train_df_x_stats_null, Oxford_train_df_x_stats_null, Manchester_train_df_y_stats_null, Oxford_train_df_y_stats_null
    if config.model_config(model_1=True):
        # creating the data frame with the x variables in model 1
        Manchester_train_df_1 = train_test_split(
            train_df[
                config.y_config(
                    y_col_name=True, y_col_num=False),
                config.x_config(
                    x_col_1_name=True, x_col_1_num=False)])
        Oxford_train_df_1 = train_test_split(
            train_df[
                config.y_config(
                    y_col_name=True, y_col_num=False),
                config.x_config(
                    x_col_1_name=True, x_col_1_num=False)])

        # describing the x and y variables of model 1
        Manchester_train_df_x_stats_1 = x_data_description(Manchester_train_df_1)
        print("Manchester Model 1 training data description (predictors): ",Manchester_train_df_x_stats_1)
        Oxford_train_df_x_stats_1 = x_data_description(Oxford_train_df_1)
        print("Oxford Model 1 training data description (predictors): ",Manchester_train_df_x_stats_1)

        Manchester_train_df_y_stats_1 = y_data_description(Manchester_train_df_1)
        print("Manchester Model 1 training data description (outcome variable): ",Manchester_train_df_y_stats_1)
        Oxford_train_df_y_stats_1 = y_data_description(Oxford_train_df_1)
        print("Oxford Model 1 training data description (outcome variable): ",Manchester_train_df_y_stats_1)


        return Manchester_train_df_1, Oxford_train_df_1, Manchester_train_df_x_stats_1, Oxford_train_df_x_stats_1, Manchester_train_df_y_stats_1, Oxford_train_df_y_stats_1
