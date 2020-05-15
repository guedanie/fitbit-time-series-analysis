import pandas as pd
import numpy as numpy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import acquire

def read_file_names():
    path = '.'
    extension = 'csv'
    os.chdir(path)
    result = glob.glob('*.{}'.format(extension))
    return result


def create_merged_df(result):
    df = pd.DataFrame([])
    df_1 = pd.DataFrame([])
    for i, elem in enumerate(result):
        rows = acquire.read_csv_file(elem)
        calories = acquire.get_calories(rows)
        df = pd.concat([df, calories])
        activities = acquire.get_activities(rows)
        df_1 = pd.concat([df_1, activities])
    return df, df_1

def merge_activty_and_calories(df, df_1):
    fitbit = pd.concat([df,df_1], axis=1)
    return fitbit

# ____ Main Prep Function ___ # 

def wrangle_fitbit_data():

    result = read_file_names()

    df, df_1 = create_merged_df(result)

    fitbit = merge_activty_and_calories(df, df_1)

    # Fill null values in the last three weeks of december
    for col in fitbit:
        fitbit[col] = fitbit[col].fillna(fitbit["2018-11-28":][col].mean())

    # Reindex the index to fill the gap between aug and september
    r = pd.date_range(start=fitbit.index.min(), end=fitbit.index.max())

    fitbit = fitbit.reindex(r)
    
    # Impude new gaps with the mean of the previous month (aug)
    for col in fitbit:
        impude_value = fitbit["2018-08"][col].resample("M").mean()[0]
        fitbit[col] = fitbit[col].fillna(impude_value)

    # replace calories
    # mean_cal = fitbit[fitbit.calories > 0].calories.mean()
    fitbit.calories = fitbit.calories.replace(0, 2000)

    return fitbit


def split_time_data_ptc(df, ptc):
    # Percentage-Based
    train_size = ptc
    n = df.shape[0]
    test_start_index = round(train_size * n)

    train = df[:test_start_index] # everything up (not including) to the test_start_index
    test = df[test_start_index:] # everything from the test_start_index to the end
    
    return train, test

def plot_splits(train, validate, test, target_variable):
    sns.lineplot(data=train, x=train.index, y= target_variable)
    sns.lineplot(data=validate, x=validate.index, y= target_variable)
    sns.lineplot(data=test, x=test.index, y= target_variable)



