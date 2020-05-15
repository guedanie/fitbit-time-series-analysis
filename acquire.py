import csv
import pandas as pd
from datetime import timedelta, datetime
import numpy as np

def read_csv_file(filename):
    fields = [] 
    rows = [] 

    # reading csv file 
    with open(filename, 'r') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
        
        # extracting field names through first row 
        fields = next(csvreader) 
    
        # extracting each data row one by one 
        for row in csvreader: 
            rows.append(row) 
    
    return rows

def get_calories(rows):
    calories = []
    date = []
    i = 0
    while rows[i] != []:
        calories.append(rows[i])
        i += 1
    calories = pd.DataFrame(calories, columns=["Date", "calories"])
    calories = calories.drop(0).reset_index().drop(columns="index")
    calories['Date'] = pd.to_datetime(calories['Date'])
    calories = calories.sort_values("Date").set_index("Date")
    calories = calories.apply(lambda x: x.str.replace(',',''))
    calories = calories.astype("float")
    return calories

# Get activities

def get_activities(rows):
    activities = []
    i = (rows.index(["Activities"]) +1)
    while rows[i] != []:
        activities.append(rows[i])
        i += 1

    activities = pd.DataFrame(activities)

    activities.columns=(activities[:1].values[0])

    activities.drop(0, inplace=True)

    activities['Date'] = pd.to_datetime(activities['Date'])
    activities = activities.sort_values("Date").set_index("Date")
    activities = activities.apply(lambda x: x.str.replace(',',''))
    activities = activities.astype("float")

    return activities

# Get food_logs
def get_food_logs(rows):
    indices = []
    for i, elem in enumerate(rows):
        if rows[i] != []:

            if 'Food Log' in rows[i][0]:
                indices.append(i)

    food_logs = pd.DataFrame(rows[indices[0]:])
    
    # Only need it if file name is ""2018-05-27_through_2018-06-26.csv""
    # food_logs = food_logs.drop([41,42,43,44,45]).reset_index().drop(columns="index")

    food_logs["date"] = np.nan

    dates = food_logs[0].unique()

    dates = np.delete(dates, [1,3])

    dates = np.delete(dates, [1])

    n_rows_start = 0
    n_rows_end = 9
    for i in range(0,food_logs[0].str.contains("Food Log").sum()):
        food_logs.loc[n_rows_start:n_rows_end, "date"] = dates[i]
        n_rows_start += 10
        n_rows_end += 10


    # Now I can drop column 0, and I need to break the date column and change it to data type
    

    food_logs.date = food_logs.date.str.slice(9,)

    food_logs['date'] = pd.to_datetime(food_logs['date'])

    food_logs = food_logs.dropna().set_index("date").rename(columns = {1:"Measure", 2: "Quantity"}).drop(columns= [0])

    food_logs.Quantity = food_logs.Quantity.str.replace("mg", '').str.replace("g", '').str.replace("fl oz", '').str.replace("Calories", "").str.replace(',', '').str.replace(' ', '')

    food_logs.Quantity = food_logs.Quantity.astype("int")
    
    food_logs[food_logs.Quantity == ''] = np.nan

    food_logs = food_logs.dropna()
      

    food_logs = pd.pivot_table(data=food_logs, values="Quantity", index =food_logs.index, columns="Measure")
    
    return food_logs


def get_food_logs_special(rows):
    indices = []
    for i, elem in enumerate(rows):
        if rows[i] != []:

            if 'Food Log' in rows[i][0]:
                indices.append(i)

    food_logs = pd.DataFrame(rows[indices[0]:])
    
    # Only need it if file name is ""2018-05-27_through_2018-06-26.csv""
    food_logs = food_logs.drop([41,42,43,44,45]).reset_index().drop(columns="index")

    food_logs["date"] = np.nan

    dates = food_logs[0].unique()

    dates = np.delete(dates, [1,3])

    dates = np.delete(dates, [1])

    n_rows_start = 0
    n_rows_end = 9
    for i in range(0,food_logs[0].str.contains("Food Log").sum()):
        food_logs.loc[n_rows_start:n_rows_end, "date"] = dates[i]
        n_rows_start += 10
        n_rows_end += 10


    # Now I can drop column 0, and I need to break the date column and change it to data type
    

    food_logs.date = food_logs.date.str.slice(9,)

    food_logs['date'] = pd.to_datetime(food_logs['date'])

    food_logs = food_logs.dropna().set_index("date").rename(columns = {1:"Measure", 2: "Quantity"}).drop(columns= [0])

    food_logs.Quantity = food_logs.Quantity.str.replace("mg", '').str.replace("g", '').str.replace("fl oz", '').str.replace("Calories", "").str.replace(',', '').str.replace(' ', '')

    food_logs.Quantity = food_logs.Quantity.astype("int")
    
    food_logs[food_logs.Quantity == ''] = np.nan

    food_logs = food_logs.dropna()

    food_logs = pd.pivot_table(data=food_logs, values="Quantity", index =food_logs.index, columns="Measure")
    
    return food_logs

def get_data(filename):
    rows = read_csv_file(filename)
    calories = get_calories(rows)
    activities = get_activities(rows)

    # if filename == "2018-05-27_through_2018-06-26.csv":
    #     food_logs = get_food_logs_special(rows)
    # else:
    #     food_logs = get_food_logs(rows)
    
    return calories, activities
