import config 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def train_test_split(df_xy):
    ''' This function splits the dataframe into a training and test dataset with 
    80% of the data in the training dataset '''
    train_df = df_xy.sample(frac=0.8,random_state=0)
    test_df = df_xy.drop(train_df.index)
    
    return train_df, test_df

def x_data_description(train_df):
    # removing the y variable from the dataframe using the config file
    train_df_y = train_df.pop(config.y_config(y_col_num=False, y_col_name=True))
    train_df_x_stats = train_df.describe()
    # transposing the results to have the descriptive statistics as columns
    train_df_x_stats = train_df_x_stats.transpose()
    return train_df, train_df_y, train_df_x_stats

def y_data_description(train_df_y):
    train_df_y_stats = (train_df_y.describe().transpose())

    # transposing the results to have the descriptive statistics as columns
    return train_df_y, train_df_y_stats

def data_description(train_df, model_null, model_1):
    if config.model_config(model_null==True, model_1==False):
        #describing the x and y variables of the null model 
        train_df_x_null, train_df_y_null, train_df_x_stats_null = x_data_description(train_df)
        print("Null Model train dataset x variables: ",train_df_x_null)
        print("Null Model training data description (predictors): ",train_df_x_stats_null)
        train_df_y_null, train_df_y_stats_null = y_data_description(train_df_y_null)
        print("Null Model train dataset y variables: ",train_df_y_null)
        print("Null Model training data description (outcome variable): ",train_df_y_stats_null)

        return train_df_x_null, train_df_y_null, train_df_x_stats_null, train_df_y_stats_null
    if config.model_config(model_1==True, model_null==False):
        # describing the x and y variables of model 1
        train_df_x_1, train_df_y_1, train_df_x_stats_1 = x_data_description(train_df)
        print("Model 1 training data description (predictors): ",train_df_x_stats_1)
        print("Model 1 train dataset x variables: ",train_df_x_1)
        train_df_y_1, train_df_y_stats_1 = y_data_description(train_df_y_1)
        print("Model 1 training data description (outcome variable): ",train_df_y_stats_1)
        print("Model 1 train dataset y variables: ",train_df_y_1)

        return train_df_x_1, train_df_y_1, train_df_x_stats_1, train_df_y_stats_1

def norm(train_df, train_df_x_stats, model_null, model_1):
    norm_train_df = (train_df - train_df_x_stats['mean']) / train_df_x_stats['std']
    return norm_train_df

def build_model(norm_train_df, train_df_x_stats, model_null, model_1):
    if config.model_config(model_null=True, model_1=False):
        norm_train_df = norm(norm_train_df, train_df_x_stats, model_null=True, model_1=False)
    if config.model_config(model_null=False, model_1=True):
        norm_train_df = norm(norm_train_df, train_df_x_stats, model_null=False, model_1=True)

    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(norm_train_df.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
    model.summary()

    return model