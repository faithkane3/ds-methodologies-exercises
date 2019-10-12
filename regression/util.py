from env import host, user, password

# function 
def get_db_url(db_name):
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

# function looks strips spaces, replaces them with NANs, and converts them to a float
def space_to_float(df, column):
    df.column = df.total_charges.str.strip().replace(" ",np.nan).astype(float)
    return df

def wrangle_df(df, col):
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df[col] = df[col].astype('float')
    df = df.dropna()
    return df

def read_sql_query(db, query, url):
    url = get_db_url(db)
    df = pd.read_sql(query, url)
    return df