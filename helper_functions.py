import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as scs
import numpy as np
from numpy import std, mean, sqrt



def connection(data='Northwind_small.sqlite'):
    """
    Establishes a connection to the database and returns a cursor and connection
    """
    conn = sqlite3.connect(data)
    cursor = conn.cursor()
    return conn, cursor

def get_tables(curr):
    """
    Returns a list of the table names in the current working database
    """
    return curr.execute('select name from sqlite_master where type="table"').fetchall()

def get_table(conn, table=None):
    """
    Returns a pandas dataframe from the specified query
    """
    df = pd.read_sql(f'select * from {table}', conn)
    return df


def get_hist(data1, data2, label1=None, label2=None, gr_label_x=None, gr_label_y=None, bins=30):
    """
    Plots a histogram of the data provided
    """
    plt.figure(figsize=(13, 8))
    plt.grid()
    plt.hist(data1, bins=bins, label=label1, color='purple', alpha=0.5)
    plt.hist(data2, bins=bins, label=label2, color='g', alpha=0.5)
    plt.legend()
    plt.xlabel(gr_label_x)
    plt.ylabel(gr_label_y)
    plt.show()

def test_equal_variance(x1, x2):
    """
    Runs a Levene test for equal variances. Returns the P value with an interpretation.
    """
    t, p = scs.levene(x1, x2)
    if p < 0.05:
        print(f'p= {p}\n Variances are not equal.')
        return False
    print(f'p= {p}\n Variances are equal.')
    return True
         
def test_normality(x):
    """
    Runs a Shapiro test for normal distribution. Returns the P value and an interpration.
    """
    t, p = scs.shapiro(x)
    if p < 0.05 :
        print(f'p= {p}\n The data is not normally distributed.')
        return False
    print(f'p= {p}\n The data is normally distributed.')
    return True

def sampling_means(data1=None, data2=None, samps=30):
    """
    Performs a sampling means with the data provided.  Returns 2 separate arrays.
    """
    d1 = []
    d2 = []
    for i in range(samps):
        data1_samp = np.random.choice(data1, size=data1.shape[0], replace=True).mean()
        d1.append(data1_samp)
        
        data2_samp = np.random.choice(data2, size=data2.shape[0], replace=True).mean()
        d2.append(data2_samp)
    return d1, d2

def calc_effect(x,y):
    """
    Calculates the effect size
    """
    lx = len(x)
    ly = len(y)
    dof = lx + ly -2
    return (mean(x) - mean(y)) / sqrt(((lx-1)* std(x, ddof=1) ** 2 + (ly-1)* std(y, ddof=1) ** 2) / dof)

def query_to_df(query=None, conn=None):
    """
    Returns a Pandas DataFrame of the provided query
    """
    return pd.read_sql(query, conn)