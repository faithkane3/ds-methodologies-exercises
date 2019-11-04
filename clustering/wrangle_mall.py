import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
import env

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# get mall customer data

def get_mallcustomer_data():
    df = pd.read_sql('SELECT * FROM customers;', get_connection('mall_customers'))
    return df.set_index('customer_id')

# summarize mall customer data

def df_summary(df):
    print('--- Shape: {}'.format(df.shape))
    print('--- Info')
    df.info()
    print('--- Descriptions')
    print(df.describe(include='all'))

# handle outliers in the data

def remove_outliers_iqr(df, columns, k):
    for col in columns:
        q75, q25 = np.percentile(df[col], [75,25])
        ub = k*stats.iqr(df[col]) + q75
        lb = q25 - k*stats.iqr(df[col])
        df = df[df[col] <= ub]
        df = df[df[col] >= lb]
    return df

# split the data

def split(df, target, train_prop, seed):
    return train_test_split(df, train_size=train_prop, stratify=df[target], random_state=seed)

# scale the data

def scale_minmax(x_train, x_test, column_list):
    scaler = MinMaxScaler()
    column_list_scaled = [col + '_scaled' for col in column_list]
    x_train_scaled = pd.DataFrame(scaler.fit_transform(x_train[column_list]), 
                                columns = column_list_scaled, 
                                index = x_train.index)
    x_train = x_train.join(x_train_scaled)
    x_test_scaled = pd.DataFrame(scaler.transform(x_test[column_list]), 
                                columns = column_list_scaled, 
                                index = x_test.index)
    x_test = x_test.join(x_test_scaled)
    return x_train, x_test, scaler

# encode the data

def one_hot_encode(train, test, col_name):
    encoded_values = sorted(list(train[col_name].unique()))

    # create 2D np arrays of the encoded variable (in train and test)
    train_array = np.array(train[col_name]).reshape(len(train[col_name]),1)
    test_array = np.array(test[col_name]).reshape(len(test[col_name]),1)

    # One Hot Encoding
    ohe = OneHotEncoder(sparse=False, categories='auto')
    train_ohe = ohe.fit_transform(train_array)
    test_ohe = ohe.transform(test_array)

    # Turn the array of new values into a data frame with columns names being the values
    # and index matching that of train/test
    # then merge the new dataframe with the existing train/test dataframe
    train_encoded = pd.DataFrame(data=train_ohe,
                            columns=encoded_values, index=train.index)
    train = train.join(train_encoded)

    test_encoded = pd.DataFrame(data=test_ohe,
                               columns=encoded_values, index=test.index)
    test = test.join(test_encoded)

    return train, test