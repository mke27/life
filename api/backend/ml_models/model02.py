from backend.db_connection import db
import numpy as np
import pandas as pd
import logging

from flask import current_app


def autoregressor(df):
    """
    Gives the x and y vector for the autoregressive model predicting QoL with a 5 year lag

    args:
        - df: dataframe of unstandardized QoL values, country, and year
    
    returns:
        - [X, y]: list of numpy arrays X (X matrix w/ 26 country indicator cols and 5 QoL lag cols)
            and y (y vector w/ last 7 years of QoL scores for each EU country)

    """
    p = 5
    eu_countries = [
                " country_name_Austria", " country_name_Belgium", " country_name_Bulgaria", " country_name_Croatia", " country_name_Cyprus", " country_name_Czechia", " country_name_Denmark",
                " country_name_Estonia", " country_name_Finland", " country_name_France", " country_name_Germany", " country_name_Greece", " country_name_Hungary", " country_name_Ireland",
                " country_name_Italy", " country_name_Latvia", " country_name_Lithuania", " country_name_Luxembourg", " country_name_Malta", " country_name_Netherlands",
                " country_name_Poland", " country_name_Portugal", " country_name_Romania", " country_name_Slovakia", " country_name_Slovenia", " country_name_Spain"
            ]

    df_encoded = pd.get_dummies(df, columns=[' country_name'], dtype = 'int')

    X = []
    y = []

    for country in df[' country_name'].unique(): 

        mask = df[' country_name'] == country
        df_country = df_encoded[mask].sort_values(' score_year')

        qol_country = df_country[' qol_score'].to_numpy()
        dummy_country = df_country[eu_countries].to_numpy()[0]

        for t in range(p, len(qol_country)):
            lags = qol_country[t - p:t][::-1] 
            
            row = np.concatenate([dummy_country, lags])
            X.append(row)
            y.append(qol_country[t])

    X = np.array(X)
    y = np.array(y)

    return [X, y]

def linreg(X, y):
    """
    Returns weight vector for autoregressive model

    args: 
        - X: X matrix w/ 26 country indicator cols and 5 QoL lag cols
        - y: y vector w/ last 7 years of QoL scores for each EU country

    returns: 
        - w: weight vector 
    """
    XtXinv = np.linalg.inv(np.matmul(X.T, X))
    w = np.matmul(XtXinv, np.matmul(X.T, y))

    return w

def predict(y, w, country, target_year):
    """
    Predicts future QoL for a given country and year

    args:
        - y: y vector w/ last 7 years of QoL scores for each EU country
        - w: weight vector
        - country: string country name
        - target_year: numerical year to predict for

    returns: 
        - pred: prediction for QoL for given country and year
    """
    country_list = [
                "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark",
                "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland",
                "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
                "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"
            ]
    values_per_country = 7
    p = 5

    # creating one-hot encoding columns
    if country == "Sweden":
        startX = np.zeros(len(country_list) - 1)
    else:
        country_index = country_list.index(country)
        startX = np.zeros(len(country_list) - 1)
        startX[country_index] = 1

    base_index = country_list.index(country)  
    start = base_index * values_per_country + 2
    end = start + 5
    endY = y[start:end][::-1].tolist()

    current_year = 2023
    
    while current_year <= target_year:
        row = np.concatenate([startX, endY])
        X = np.array(row)
        pred = np.dot(X, w)
        endY = [pred] + endY[:p - 1]  
        current_year += 1
    
    return pred

def train():
  """
  You could have a function that performs training from scratch as well as testing (see below).
  It could be activated from a route for an "administrator role" or something similar. 
  """
  return 'Training the model'

def test():
  return 'Testing the model'

def predict_table(input_country):
  """
  Retreives model parameters from the database and predicts QoL score for next five years 
  and returns a dataframe of year and predicted QoL score
  """
  # get a database cursor 
  cursor = db.get_db().cursor()
  # get the model params from the database
  query = 'SELECT country_name, score_year, qol_score FROM ML_Score_US'
  cursor.execute(query)
  return_val = cursor.fetchall()

  df = pd.DataFrame.from_dict(return_val)

  matrices = autoregressor(df)
  X = matrices[0]
  y = matrices[1]
  w = linreg(X, y)
  years = list(range(2023, 2028))  
  predictions = []
  
  for year in years:
    pred = predict(y, w, input_country, year)
    predictions.append({'year': year, 'prediction': pred})
    
    pred_df = pd.DataFrame(predictions)
    
    return pred_df