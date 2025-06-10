from backend.db_connection import db
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from flask import current_app

# building vectors for autoregresssion
def autoregressor():
    """
    Gives the x and y vector for the autoregressive model predicting QoL with a 5 year lag

    args:
        - df: dataframe of unstandardized QoL values, country, and year
    
    returns:
        - [X, y]: list of numpy arrays X (X matrix w/ 26 country indicator cols and 5 QoL lag cols)
            and y (y vector w/ last 7 years of QoL scores for each EU country)

    """
    # get a database cursor 
    cursor = db.get_db().cursor()
    # get the model params from the database
    query = 'SELECT country_name, score_year, qol_score FROM ML_Score_US'
    cursor.execute(query)
    return_val = cursor.fetchall()

    df = pd.DataFrame.from_dict(return_val)

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

# performing linear regression
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

# making predictions
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

# creating table of predicted scores for a country
def prediction_table(y, w, country):
    """
    Predicts QoL score for next five years and returns a dataframe of year and predicted QoL score

    args:
        - country: string target country name

    returns: 
        - pred_df: dataframe of next five years of QoL scores for inputted country
    """
    years = list(range(2023, 2028))  
    predictions = []

    for year in years:
        pred = predict(y, w, country, year)
        predictions.append({'year': year, 'predictions': pred})

    pred_df = pd.DataFrame(predictions)       

    return pred_df

# combining predicted and historical scores
def qol_df(old_df, pred_df, country):
    """
    Creates a dataframe with existing and predicted QoL scores for a particular country.
    Returns a single column 'qol_score' with an indicator 'predicted'
    """
    actual = old_df[old_df[" country_name"] == country][[" score_year", " qol_score"]].copy()
    actual.columns = ["year", "qol_score"]
    actual["Projected?"] = "Historical Score"

    predicted = pred_df.copy()
    predicted.columns = ["year", "qol_score"]
    predicted["Projected?"] = "Projected Score"

    merged = pd.concat([actual, predicted], ignore_index=True)
    merged = merged.sort_values("year").reset_index(drop=True)

    return merged

# plotting historical and predicted qol for a country
def plot_qol(qol_data, country):
    """
    Plots actual and predicted QoL scores over time for a single country
    
    Args:
        - qol_data: DataFrame with 'year', 'qol_score', and 'Projected?'
        - country: Name of the country (str)
    """  
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=qol_data['year'],
        y=qol_data['qol_score'],
        mode='lines+markers',
        name='QoL Score',
        line=dict(color='royalblue'),
        customdata=qol_data[['Projected?']], 
        hovertemplate=
            'Year: %{x}<br>' +
            'QoL Score: %{y:.3f}<br>' +
            'Projected?: %{customdata[0]}<extra></extra>'
    ))

    fig.add_vline(x=2022.5, line_width=2, line_dash="dash", line_color="gray")

    fig.add_vrect(
        x0=2023, x1=qol_data['year'].max(),
        fillcolor="lightgray", opacity=0.3,
        layer="below", line_width=0,
        annotation_text="Predicted", annotation_position="top left"
    )

    fig.update_layout(
        title= f"Quality of Life (Historical and Projected) for {country}",
        xaxis_title="Year",
        yaxis_title="Quality of Life Score",
        hovermode="x unified"
    )

    fig.show()

