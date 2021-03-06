import pandas as pd 
import numpy as np 
from env import host, user, password

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler

# acquire data using sql query

def get_db_url(db_name):
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

def get_data_from_sql():
    query = """
        SELECT *
        FROM customers
        JOIN contract_types USING(contract_type_id)
        JOIN internet_service_types USING(internet_service_type_id)
        JOIN payment_types USING(payment_type_id);
    """
    df = pd.read_sql(query, get_db_url("telco_churn"))
    return df


def clean_data(df):
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df["total_charges"] = df["total_charges"].astype('float')
    df = df.dropna()
    return df


# explore data

def peekatdata(df):
    print("DataFrame Shape:\n")
    print(df.shape)
    print("\nInfo about:\n")
    print(df.info())
    print("\nDescribe:\n")
    print(df.describe())
    print("\nHead Preview:\n")
    print(df.head())
    print("\nTail Preview:\n")
    print(df.tail())


def df_value_counts(df):
    valcount_df = pd.DataFrame(df.apply(lambda x: x.value_counts(dropna=False).count()))
    return valcount_df


def percent_missing(df):
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    return df.isnull().sum() / len(df) * 100

# split the data

def split(df, target, train_prop, seed):
    return train_test_split(df, train_size=train_prop, stratify=df[target], random_state=seed)

# impute the data if desired

def impute(train, test, my_strategy, column_list):
    imputer = SimpleImputer(strategy=my_strategy)
    train[column_list] = imputer.fit_transform(train[column_list])
    test[column_list] = imputer.transform(test[column_list])
    return train, test, imputer

# encode the data

def encode(train, test, col_name):
    encoded_values = sorted(list(train[col_name].unique()))
    
    # Integer Encoding
    int_encoder = LabelEncoder()
    train.encoded = int_encoder.fit_transform(train[col_name])
    test.encoded = int_encoder.transform(test[col_name])
    
    # create 2D np arrays of the encoded variable (in train and test)
    train_array = np.array(train.encoded).reshape(len(train.encoded),1)
    test_array = np.array(test.encoded).reshape(len(test.encoded),1)

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
    return train, test, int_encoder, ohe

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


# prepare the data using 

def prepare(df, drop_cols, float_cols, obj_cols, target, train_prop, seed, impute_cols, impute_strategy, encode_col, scale_cols):
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df = df.dropna()
    df[float_cols] = df[float_cols].astype(float)
    df[obj_cols] = df[obj_cols].astype(object)
    df.drop(columns=drop_cols, inplace=True)
    train, test = split(df=df, target=target, train_prop=train_prop, seed=seed)
    train, test, imputer = impute(train, test, my_strategy=impute_strategy, column_list=impute_cols)
    train, test, int_encoder, ohe = encode(train, test, col_name = encode_col)
    train, test, scaler = scale_minmax(train, test, column_list = scale_cols)
    return df, train, test, imputer, int_encoder, ohe, scaler