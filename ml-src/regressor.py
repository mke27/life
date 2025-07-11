# time series auto regression model data pipeline

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('datasets/preprocessed-datasets/alldata_unstandard.csv')

# building vectors for autoregresssion
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
    start = base_index * values_per_country 
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
def prediction_table(country):
    """
    Predicts QoL score for next five years and returns a dataframe of year and predicted QoL score

    args:
        - country: string target country name

    returns: 
        - pred_df: dataframe of next five years of QoL scores for inputted country
    """
    matrices = autoregressor(df)
    X = matrices[0]
    y = matrices[1]
    w = linreg(X, y)
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

# plots testing linearity
def linearity_plots(df, lag_index):
    """
    Creates plots testing the linearity of the autoregressive model
    """
    results = loocv_autoreg(df)
    resids = results['residuals']

    matrices = autoregressor(df)
    X_all = matrices[0]

    lag_col = 26 + lag_index - 1  
    x_feature = [x[lag_col] for x in X_all]

    # resids vs. x vals
    plt.scatter(x_feature, resids, alpha=0.5)
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel(f'QoL Lag {lag_index} Year(s) Ago')
    plt.ylabel('Residuals')
    plt.title(f'Residuals vs QoL Lag {lag_index} Year(s) Ago')
    plt.show()

    # reisds vs. order
    plt.figure(figsize=(10, 5))
    plt.plot(resids, marker='o', linestyle='-', alpha=0.7)
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel('Index/Order')
    plt.ylabel('Residuals')
    plt.title('Residuals vs. Order')
    plt.show()

    # resids histogram
    sns.histplot(resids, kde=False)
    plt.xlabel("Residuals")
    plt.title("Residuals Histogram")
    plt.show()

# combined data pipeline
def autoregressor_all(df, input_country):
    """
    Given a country, predicts next five years of QoL scores and returns a graph of historical and predicted scores

    args:
        - input_country: country name

    returns:
        - None, graphs historical and predicted QoL
    """

    eu_countries = [
                " country_name_Austria", " country_name_Belgium", " country_name_Bulgaria", " country_name_Croatia", " country_name_Cyprus", " country_name_Czechia", " country_name_Denmark",
                " country_name_Estonia", " country_name_Finland", " country_name_France", " country_name_Germany", " country_name_Greece", " country_name_Hungary", " country_name_Ireland",
                " country_name_Italy", " country_name_Latvia", " country_name_Lithuania", " country_name_Luxembourg", " country_name_Malta", " country_name_Netherlands",
                " country_name_Poland", " country_name_Portugal", " country_name_Romania", " country_name_Slovakia", " country_name_Slovenia", " country_name_Spain"
            ]
    country_list = [
                "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark",
                "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland",
                "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
                "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"
            ]
    values_per_country = 7
    p = 5

    df_encoded = pd.get_dummies(df, columns=[' country_name'], dtype='int')

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

    XtXinv = np.linalg.inv(np.matmul(X.T, X))
    w = np.matmul(XtXinv, np.matmul(X.T, y))

    # creating one-hot encoding columns
    startX = np.zeros(len(eu_countries))
    input_eu_country_names = [c.replace(" country_name_", "") for c in eu_countries]
    if input_country in input_eu_country_names:
        country_index = input_eu_country_names.index(input_country)
        startX[country_index] = 1
    else:
        startX = np.zeros(len(country_list) - 1)

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
            X = np.array(row)
            pred = np.dot(X, w)
            endY = [pred] + endY[:p - 1]
            predictions.append({'year': current_year, 'predictions': pred})
            current_year += 1

    pred_df = pd.DataFrame(predictions)

    actual = df[df[" country_name"] == input_country][[" score_year", " qol_score"]].copy()
    actual.columns = ["year", "qol_score"]

    predicted = pred_df.copy()
    predicted.columns = ["year", "qol_score"]

    merged = pd.concat([actual, predicted], ignore_index=True)
    merged = merged.sort_values("year").reset_index(drop=True)

    merged_dict = merged.to_dict(orient="records")

    return merged_dict

# plotting historical and predicted qol for a country
def plot_qol(qol_data, country, qol_data2 = None, country2 = None):
    """
    Plots actual and predicted QoL scores over time for a single country
    
    Args:
        - qol_data: list of dicts with keys 'year' and 'qol_score'
        - country: Name of the country (str)
    """  
    historical_years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    predicted_years = [2023, 2024, 2025, 2026, 2027]

    qol_df = pd.DataFrame(qol_data)

    qol_df["Projected?"] = "Unknown"  

    qol_df.loc[qol_df["year"].isin(historical_years), "Projected?"] = "Historical Score"
    qol_df.loc[qol_df["year"].isin(predicted_years), "Projected?"] = "Predicted Score"

    fig = go.Figure()

    qol_df = pd.DataFrame(qol_data)
    qol_df["Source"] = qol_df["year"].apply(
        lambda y: "Historical Score" if y in historical_years else (
            "Predicted Score" if y in predicted_years else "Unknown"
        )
    )

    fig.add_trace(go.Scatter(
        x=qol_df['year'],
        y=qol_df['qol_score'],
        mode='lines+markers',
        name=f'{country} QoL',
        line=dict(color='royalblue'),
        customdata=qol_df[["Source"]],
        hovertemplate=
            f'<b>{country}</b><br>' +
            'Year: %{x}<br>' +
            'QoL Score: %{y:.3f}<br>' +
            'Type: %{customdata[0]}<extra></extra>'
    ))

    if qol_data2 is not None and country2 is not None:
        qol_df2 = pd.DataFrame(qol_data2)
        qol_df2["Source"] = qol_df2["year"].apply(
            lambda y: "Historical Score" if y in historical_years else (
                "Predicted Score" if y in predicted_years else "Unknown"
            )
        )

        fig.add_trace(go.Scatter(
            x=qol_df2['year'],
            y=qol_df2['qol_score'],
            mode='lines+markers',
            name=f'{country2} QoL',
            line=dict(color='crimson'),
            customdata=qol_df2[["Source"]],
            hovertemplate=
                f'<b>{country2}</b><br>' +
                'Year: %{x}<br>' +
                'QoL Score: %{y:.3f}<br>' +
                'Type: %{customdata[0]}<extra></extra>'
        ))

    fig.add_vline(x=2022.5, line_width=2, line_dash="dash", line_color="gray")

    fig.add_vrect(
        x0=2023, x1=max(
            qol_df['year'].max(),
            qol_df2['year'].max() if qol_data2 else 2027
        ),
        fillcolor="lightgray", opacity=0.3,
        layer="below", line_width=0,
        annotation_text="Predicted", annotation_position="top left"
    )

    fig.update_layout(
        title="Quality of Life (Historical and Projected)",
        xaxis_title="Year",
        yaxis_title="Quality of Life Score"
    )

    fig.show()















    
    
