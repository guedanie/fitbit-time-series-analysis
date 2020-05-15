# data manipulation 
import numpy as np
import pandas as pd

from datetime import datetime
from sklearn import metrics
from sklearn.metrics import mean_squared_error
import sklearn

# data visualization 
import matplotlib.pyplot as plt
import seaborn as sns

import explore
import acquire
import prepare

from math import sqrt

from statsmodels.tsa.api import Holt



def create_predictions_df(train, validate, target_variable):

    baseline = round(train[target_variable][-1:][0], 2)

    predictions = pd.DataFrame({
    "actual": validate[target_variable], 
    "baseline": [baseline]},
    index = validate.index)

    return predictions

# ------------ #
#   Modeling   #
# ------------ #

def run_simple_average(train, target_variable):
    y_pred = round(train[target_variable].mean(), 2)
    return y_pred 

def run_moving_average(train, target_variable, rolling_average):
    y_pred = round(train[target_variable].rolling(rolling_average).mean().iloc[-1], 2)
    return y_pred


def run_holts(train, validate, target_variable, smoothing_level = .1, smoothing_slope = .1):
    # Create model object
    model = Holt(train[target_variable], exponential = True)

    # Fit model 
    model = model.fit(smoothing_level = smoothing_level, smoothing_slope=smoothing_slope, optimized = False)

    # Create predictions
    y_pred = model.predict(start=validate.index[0], end=validate.index[-1])

    return model, y_pred

# ---------------- #
#     Evaluate     #
# ---------------- # 

def print_rmse(model, predictions):
    print(f'RMSE = {round(sqrt(mean_squared_error(predictions.actual, predictions[model])), 0)}')

def plot_prediction(model, target_variable, train, validate, predictions):
    plt.figure(figsize = (20, 9))

    sns.lineplot(data=train, x=train.index, y=target_variable)
    sns.lineplot(data=validate, x=validate.index, y=target_variable)
    sns.lineplot(data=predictions, x=predictions.index, y=model)

def plot_rmse(predictions):
    rmse = predictions.apply(lambda col: sqrt(sklearn.metrics.mean_squared_error(predictions.actual, col)))
    rmse.plot.bar()