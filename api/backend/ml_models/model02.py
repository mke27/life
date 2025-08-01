from backend.db_connection import db
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import requests

from flask import current_app

def autoregressor_all(input_country):
    """
    Given a country, predicts next five years of QoL scores and returns a graph of historical and predicted scores

    args:
        - input_country: country name

    returns:
        - None, graphs historical and predicted QoL
    """
    # get a database cursor 
    cursor = db.get_db().cursor()
    # get the model params from the database
    query = 'SELECT country_name, score_year, qol_score FROM ML_Score_US'
    cursor.execute(query)
    return_val = cursor.fetchall()

    df = pd.DataFrame.from_dict(return_val)

    eu_countries = [
                "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark",
                "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland",
                "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
                "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain"
            ]
    country_list = [
                "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark",
                "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland",
                "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
                "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"
            ]
    values_per_country = 7
    p = 5

    df_encoded = pd.get_dummies(df, columns=['country_name'], prefix='', prefix_sep='', dtype='int')

    X = []
    y = []

    for country in df['country_name'].unique():

        mask = df['country_name'] == country
        df_country = df_encoded[mask].sort_values('score_year')

        qol_country = df_country['qol_score'].to_numpy()
        dummy_country = df_country[eu_countries].to_numpy()[0]

        for t in range(p, len(qol_country)):
            lags = qol_country[t - p:t][::-1]

            row = np.concatenate([dummy_country, lags])
            X.append(row)
            y.append(qol_country[t])

    X = np.array(X)
    y = np.array(y)

    response = requests.get("http://web-api:4000/model/weights")
    w = np.array(response.json(), dtype=float)

    # creating one-hot encoding columns
    startX = np.zeros(len(eu_countries))
    input_eu_country_names = [c.replace("country_name_", "") for c in eu_countries]
    if input_country in input_eu_country_names:
        country_index = input_eu_country_names.index(input_country)
        startX[country_index] = 1

    base_index = country_list.index(input_country)
    start = base_index * values_per_country
    end = start + 5
    endY = y[start:end][::-1].tolist()

    prediction_years = [2023, 2024, 2025, 2026, 2027]
    current_year = 2023
    predictions = []

    for target_year in prediction_years:
        while current_year <= target_year:
            row = np.concatenate([startX, endY])
            X = np.array(row, dtype=float)
            pred = np.dot(X, w)
            endY = [pred] + endY[:p - 1]
            predictions.append({'year': current_year, 'predictions': pred})
            current_year += 1

    pred_df = pd.DataFrame(predictions)

    actual = df[df["country_name"] == input_country][["score_year", "qol_score"]].copy()
    actual.columns = ["year", "qol_score"]

    predicted = pred_df.copy()
    predicted.columns = ["year", "qol_score"]

    merged = pd.concat([actual, predicted], ignore_index=True)
    merged = merged.sort_values("year").reset_index(drop=True)

    merged_dict = merged.to_dict(orient="records")

    return merged_dict

