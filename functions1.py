import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy as sp
import scipy.stats as stats
from scipy.stats import zscore

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

import statsmodels.api as sm
from statsmodels.stats import diagnostic as diag
import statsmodels.stats.api as sms
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt

from scipy.stats import skew
from scipy.stats import boxcox

from math import radians, cos, sin, asin, sqrt

def std_describe(df):
    '''Retrieves the summary of a pd.DataFrame, adds a metric that represents
       3 standard deviations, and returns the summary.
    
            @params
            df is a pd.DataFrame
    
            @output
            summary of a pd.DataFrame.describe() with standard deviation metric added
    '''
    print('                  Description with |3| STD Report                          ')
    #print('-------------------------------------------------------------------------')
    desc_df = df.describe()

    desc_df.loc['+3_std'] = desc_df.loc['mean'] + (desc_df.loc['std'] * 3)
    desc_df.loc['-3_std'] = desc_df.loc['mean'] - (desc_df.loc['std'] * 3)
    print(desc_df)


def percent_null_df(df):
    ''' Prints the percentage of null values for the entire dataframe and
    in each column of a dataframe
    
    @params
    df is a pd.DataFrame
    df_percent_null is the percentage null for the entire dataframe
    x is a list of strings containing the column names for missing_data
    missing_data is a pd.Dataframe containing x columns
    columns is a list of strings that contain the names of the columns in df
    col is an instance of the list of strings columns
    icolumn_name is a string containing the name of the column
    imissing_data is the sum of null values in col
    imissing_in_percentage returns a percentage of null values in col as a float
    missing_data.loc[len(missing_data)] creates a row containing the column name and percent null
    
    @output
    a pd.DataFrame containing the names of each col in df and their percent null values
    '''
    df_percent_null = len(df.isna().sum())/len(df)*100
    print('\n                   Percent Null Report                ')
    print('--------------------------------------------------------')
    print('\n       Total Percent Null For Data Frame: ', round(df_percent_null, 3), '\n')
    x = ['column_name','missing_data', 'missing_in_percentage']
    missing_data = pd.DataFrame(columns=x)
    columns = df.columns
    for col in columns:
        icolumn_name = col
        imissing_data = df[col].isnull().sum()
        imissing_in_percentage = round((df[col].isnull().sum()/df[col].shape[0])*100, 3)
        missing_data.loc[len(missing_data)] = [icolumn_name, imissing_data, imissing_in_percentage]
    missing_data = missing_data.sort_values(by = 'missing_in_percentage', ascending=False)
    print('           Total Percent Null by Column               \n')
    print(missing_data)



def obtain_data(csv):
    '''Takes in a .csv file, prints STD Description Report and Percent Null Report
    then, returns a pd.DataFrame
    
        @params
        csv is a .csv file
        df is a pd.DataFrame
        
        @output
        a pd.Dataframe
    
    '''
    df = pd.read_csv(csv)
    print(df.info())
    print()
    print(percent_null_df(df))
    return df


# cell 3 functions
def remove_dupes(df, col):
    '''Identifies duplicates in a column in a pd.DataFrame,
    and removes the duplicates, keeping the first one
    
    @params:
    df is a pd.DataFrame
    col is a column in df
    
    
    @output
    a pd.Dataframe
    '''                       
    x = df.shape[0]
    df.sort_values(by=col, inplace=True) 
    df.drop_duplicates(subset=col, 
                     keep='first', inplace=True)
    print('          ', x-df.shape[0], 'duplicates removed. \n')
    return df


def idx_select_sort_set(df, indices):
    '''Takes in a pd.DataFrame and a list of 2 indices in order 
    of importance, selects those indices, finds and removes
    duplicates, sorts and sets the primary index.
    
        @params
        a pd.DataFrame
        
        @ output
        a pd.DataFrame
        
        '''
    print('\n                  Index Report                       ')
    print('------------------------------------------------------')
    print('              Primary Index Set as: ', indices[0])
    print('            Secondary Index Set as: ', indices[1], '\n')
          
    print('\n                Duplicate Report                  ')
    print('------------------------------------------------------')    
    x = df[df[indices[0]].duplicated(keep=False)]
    print('           ', len(x), ' duplicates found in ', indices[0])
    y = x[x[indices[1]].duplicated()]
    print('           ', len(y), ' duplicates found in ', indices[1])
    df = remove_dupes(df, indices[0])
    df = df.set_index(indices[0])
    
    return df


def find_nulls(df):
    ''' Identifies null values among each column in a pd.Dataframe, and displays
    the number of null values, unique values, and their value counts.
    
    @params:
    df is a pd.DataFrame

    @Output:
    a printed display
    '''
    
    print('\n              Null & Unique Values Report                  ')
    print('               for Columns with Null Values                  ')
    print('------------------------------------------------------')
    
    null_cols = []
    for col in df.columns:
        if df[col].isna().sum() > 0:
            null_cols.append(col)
    for col in null_cols:
        print(col)
        print('-------------')
        print('Null values: ', df[col].isna().sum())
        print('Unique values: ', len(list(df[col].unique())), '\n')
        print('Value Counts\n------------')
        print(df[col].value_counts(), '\n')     

        
def rm_outliers_by_zscore(df, cols):
    '''Takes in a pd.DataFrame and a column
    creates a new column that identifies z_score
    of the given column and then drops the rows
    in which the absolute value of the value in the 
    zscore column is greater than 3. It generates
    a report with the total number and percentage 
    of outliers removed.
    
        
        @params
        df is a pd.Dataframe
        col is a column in df
        
        @output
        df
    '''
    
    print('\n              Outlier Removal Report                  ')
    print('         for columns: ', cols                      )
    print('------------------------------------------------------')
    total_percent_removed = 0
    total_rows_removed = 0
    
    x = len(df)
    
    for col in cols:
        df[col + '_zscore'] = np.abs(stats.zscore(df[col]))
        y = df.loc[np.abs(df[col + '_zscore']) > 3]
        percent = round((len(y) * 100) / x, 3)
        
        print('\n', col, '\n-------------')
        print('Number of Outliers Removed: ', len(y))
        print(percent, '% of the total rows.\n')
        
        df = df.loc[np.abs(df[col + '_zscore']) < 3]
        
        df = df.drop([col + '_zscore'], axis=1)
        total_percent_removed += percent
        total_rows_removed += len(y)
    
    print('------------------------------------------------------------')
    print('Total percentage of data removed: ', round(total_percent_removed, 2))
    print('Total rows of data removed: ', total_rows_removed)
    print('New length of dataframe: ', len(df))
    print('------------------------------------------------------------')
    
    return df


def corr_heat_map(df, drop_cols):
    '''Returns a correlation matrix heat map of specified columns 
    of a pd.Dataframe
    
        @params
        df is a pd.DataFrame
        drop_cols is a list of columns to drop from the display
        
        @outputs
        sns.heatmap 
    '''
    
    fig, ax = plt.subplots(figsize=(12,12))
    corr = df.drop(drop_cols, axis=1).corr()
    return sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, 
           annot=True, fmt='.1g', cmap=sns.diverging_palette(220, 10, as_cmap=True))

def draw_qqplot(residual):
    '''Takes in a residual and returns an qqplot/sp.stats.probplot
        
        @params
        residual is a residual obtained from an OLS model
        
        @output
        an sp.stats.probplot/qqplot    
    '''
    
    fig, ax = plt.subplots(figsize=(6,2.5))
    _, (__, ___, r) = sp.stats.probplot(residual, plot=ax, fit=True)
    
    return fig, ax

def reg_summary(X_train, y_train):
    '''Takes in x/y training sets, fits an OLS regression model
    and returns a results summary.
    
        @params
        X_train is an x training set obtained from a train_test_split
        y_train is an x training set obtained from a train_test_split
        
        @output
        a model summary
    '''
    
    X_with_constant = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_with_constant)
    results = model.fit()
    print(results.params)
    print(results.summary())
    return results

def get_residual(X_test, y_test, results):
    '''Takes in x/y test sets, and OLS model results
   and returns a residual.
    
        @params
        X_test is an x test set obtained from a train_test_split
        y_test is an x test set obtained from a train_test_split
        results is ols model.fit()
        
        @output
        a variable representing the residual '''

    X_test = sm.add_constant(X_test)
    y_pred = results.predict(X_test)
    residual = y_test - y_pred
    return residual
        
def validate_reg_assumptions(X, X_train, X_test, y_train, y_test):
    '''Takes in the variables produced by train_test_split and
    prints the OLS summary, distplot, scatterplot, and qqplot.
    
        @params
        X is a pd.DataFrame
        X_train is an x training set obtained from a train_test_split
        y_train is an x training set obtained from a train_test_split
        X_test is an x test set obtained from a train_test_split
        y_test is an x test set obtained from a train_test_split
        
        @output
        A printed display of OLS summary, qqplot, displot, and regplot
    '''
    
    print('Retrieving OLS Summary...\n')
    results = reg_summary(X_train, y_train)
    print(results)
    
    print('\nIdentifying Residuals...\n')
    X_test = sm.add_constant(X_test)
    y_pred = results.predict(X_test)
    residual = y_test - y_pred

    print('\nVerifying Normality of Residuals...\n')
    sns.distplot(residual)
    plt.show();
    draw_qqplot(residual)
    plt.show();
    print('Mean of Residuals: ', np.mean(residual))

    print('\nDisplaying Regplot...\n')
    ax = sns.regplot(y_pred, residual, data=X,
    scatter_kws={"color": "black"}, line_kws={"color": "red"})
    plt.show()
    
def locate_it(data, long, lat, feature):
    plt.figure(figsize=(16,12))
    cmap = plt.cm.get_cmap('RdYlBu')
    sc = plt.scatter(data[long], data[lat],
                 c=data[feature], vmin=min(data[feature]),
                 vamx=max(data[feature]), alpha=0.5, s=5,
                 cmap=cmap)
    plt.colorbar(sc)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('House {} by location'.format(feature), fontsize=18)
    plt.show();
    
def haversine(list_long_lat, other):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees), in this case the 2nd point is in the 
    Pike Pine Retail Core of Seattle, WA.
    """
    lon1, lat1 = list_long_lat[0], list_long_lat[1]
    lon2, lat2 = other[0], other[1]
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km

def box_cox(df, skew_cols):
    '''
    with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    '''
    skewed_features = df[skew_cols].apply(lambda x : skew (x.dropna())).sort_values(ascending=False)

    #compute skewness
    skewness = pd.DataFrame({'Skew' :skewed_features})   

    # Get only higest skewed features
    skewness = skewness[abs(skewness) > 0.7]
    skewness = skewness.dropna()
    print ("There are {} higest skewed numerical features to box cox transform".format(skewness.shape[0]))

    l_opt = {}

    for feat in skewness.index:
        df[feat], l_opt[feat] = boxcox((df[feat]+1))

        skewed_features2 = df[skewness.index].apply(lambda x : skew (x.dropna())).sort_values(ascending=False)

        #compute skewness
        skewness2 = pd.DataFrame({'New Skew' :skewed_features2})   
        x = display(pd.concat([skewness, skewness2], axis=1).sort_values(by=['Skew'], ascending=False))
    print(x)
    
    return df

