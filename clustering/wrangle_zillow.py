import pandas as pd
import env

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# Remove any properties that are likely to be something other than a single unit properties.

def get_zillow_data():
    query = '''
    select 
    svi.`COUNTY` county,
    p.`taxamount`/p.`taxvaluedollarcnt` tax_rate,
    p.`id`,
    p.`parcelid`,
    p.`airconditioningtypeid`,
    act.`airconditioningdesc`,
	p.`architecturalstyletypeid`,
	ast.`architecturalstyledesc`,
    p.`basementsqft`,
	p.`bathroomcnt`,
    p.`bedroomcnt`,
	p.`buildingclasstypeid`,
	bct.`buildingclassdesc`,
    p.`buildingqualitytypeid`,
    p.`calculatedbathnbr`,
    p.`calculatedfinishedsquarefeet`,
    p.`decktypeid`,
    p.`finishedfloor1squarefeet`,
    p.`finishedsquarefeet12`,
    p.`finishedsquarefeet13`,
    p.`finishedsquarefeet15`,
    p.`finishedsquarefeet50`,
    p.`finishedsquarefeet6`,
    p.`fips`,
    svi.`ST_ABBR` state,
    p.`fireplacecnt`,
    p.`fullbathcnt`,
    p.`garagecarcnt`,
    p.`garagetotalsqft`,
    p.`hashottuborspa`,
    p.`heatingorsystemtypeid`,
    hst.`heatingorsystemdesc`,
    p.`latitude`,
    p.`longitude`,
    p.`lotsizesquarefeet`,
    p.`poolcnt`,
    p.`poolsizesum`,
    p.`pooltypeid10`,
    p.`pooltypeid2`,
    p.`pooltypeid7`,
    p.`propertycountylandusecode`,
    p.`propertylandusetypeid`,
    plut.`propertylandusedesc`,
    p.`propertyzoningdesc`,
    p.`rawcensustractandblock`,
    p.`regionidcity`,
    p.`regionidcounty`,
    p.`regionidneighborhood`,
    p.`regionidzip`,
    p.`roomcnt`,
	p.`storytypeid`,
	st.`storydesc`,
    p.`taxvaluedollarcnt`,
    p.`threequarterbathnbr`,
    p.`unitcnt`,
    p.`yardbuildingsqft17`,
    p.`yardbuildingsqft26`,
    p.`yearbuilt`,
    p.`numberofstories`,
    p.`fireplaceflag`,
    p.`structuretaxvaluedollarcnt`,
    p.`assessmentyear`,
    p.`landtaxvaluedollarcnt`,
    p.`taxamount`,
    p.`taxdelinquencyflag`,
    p.`taxdelinquencyyear`, 
	p.`typeconstructiontypeid`,
	tct.`typeconstructiondesc`,
    p.`censustractandblock`,
    pred.`transactiondate`,
    pred.`logerror`,
    m.`transactions`
    from 
	`properties_2017` p
    inner join `predictions_2017`  pred
    on p.`parcelid` = pred.`parcelid` 
    inner join 
	(select 
		`parcelid`, 
		max(`transactiondate`) `lasttransactiondate`, 
		max(`id`) `maxid`, 
		count(*) `transactions`
	from 
		predictions_2017
	group by 
		`parcelid`
	) m
	on 
	pred.parcelid = m.parcelid
	and pred.transactiondate = m.lasttransactiondate
    left join `propertylandusetype` plut
        on p.`propertylandusetypeid` = plut.`propertylandusetypeid`
            
    left join svi_db.svi2016_us_county svi
        on p.`fips` = svi.`FIPS`
    left join `airconditioningtype` act
        using(`airconditioningtypeid`)
    left join heatingorsystemtype hst
        using(`heatingorsystemtypeid`)
    left join `architecturalstyletype` ast
        using(`architecturalstyletypeid`)
    left join `buildingclasstype` bct
        using(`buildingclasstypeid`)
    left join `storytype` st
        using(`storytypeid`)
    left join `typeconstructiontype` tct
        using(`typeconstructiontypeid`)
    where 
        p.`latitude` is not null
        and p.`longitude` is not null
        and p.bedroomcnt > 0 and p.bathroomcnt > 0
        and plut.propertylandusetypeid = '261';
    '''
    return pd.read_sql(query, get_connection('zillow'))

# remove columns and rows

def remove_columns(df, cols_to_remove):
    df = df.drop(columns=cols_to_remove)
    return df

# handle_missing_values(df, prop_required_column, prop_required_row).  
#   - The input: a dataframe, a number between 0 and 1 that represents the proportion, for each column, of rows with non-missing values required to keep the column.  i.e. if prop_required_column = .6, then you are requiring a column to have at least 60% of values not-NA (no more than 40% missing), a number between 0 and 1 that represents the proportion, for each row, of columns/variables with non-missing values required to keep the row.  i.e. if prop_required_row = .75, then you are requiring a row to have at least 75% of variables with a non-missing value (no more that 25% missing) 
#   - The output: the dataframe with the columns and rows dropped as indicated. *Be sure to drop the columns prior to the rows in your function.*

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

# Create a function that fills missing values with 0s where it makes sense based on the attribute/field/column/variable. 

def fill_zero(df, cols):
    df.fillna(value=0, inplace=True)
    return df

# Put it all together

def data_prep(df, cols_to_remove=[], prop_required_column=.5, prop_required_row=.75):
    df = remove_columns(df, cols_to_remove)
    df = handle_missing_values(df, prop_required_column, prop_required_row)
    return df