import prepare
import acquire

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# ----------------- # 
#      Explore      #
# ----------------- #

def find_range(df):
    print('Date Range:', df.index.min(), 'to', df.index.max())

def numeric_hists(df, bins=20):
    """
    Function to take in a DataFrame, bins default 20,
    select only numeric dtypes, and
    display histograms for each numeric column
    """
    num_df = df.select_dtypes(include=np.number)
    num_df.hist(bins=bins, color='thistle')
    plt.suptitle('Numeric Column Distributions')
    plt.show()

def seasonal_decomposition(df, col, period):
    y = df[col].resample(period).mean()

    result = sm.tsa.seasonal_decompose(y)
    decomposition = pd.DataFrame({
            "y": result.observed,
        "trend": result.trend,
        "seasonal": result.seasonal,
        "resid": result.resid,
    })

    decomposition.iloc[:,1:].plot()