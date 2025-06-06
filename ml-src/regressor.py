# time series auto regression model

import pandas as pd
import numpy as np

df = pd.read_csv('datasets/preprocessed-datasets/alldata_unstandard.csv')
p = 5 
features = ['healthcare', 'education', 'safety', 'environment']
eu_countries = [
        "country_Austria", "country_Belgium", "country_Bulgaria", "country_Croatia", "country_Cyprus", "country_Czechia", "country_Denmark",
        "country_Estonia", "country_Finland", "country_France", "country_Germany", "country_Greece", "country_Hungary", "country_Ireland",
        "country_Italy", "country_Latvia", "country_Lithuania", "country_Luxembourg", "country_Malta", "country_Netherlands",
        "country_Poland", "country_Portugal", "country_Romania", "country_Slovakia", "country_Slovenia", "country_Spain"
    ]

df_encoded = pd.get_dummies(df, columns=['country'], dtype = 'int')

X = []
y = []

for country in df['country'].unique(): 

    mask = df['country'] == country
    df_country = df_encoded[mask].sort_values('year')

    qol_country = df_country['qol'].to_numpy()
    feature_data_country = df_country[features].to_numpy()
    dummy_country = df_country[eu_countries].to_numpy()[0]

    for t in range(p, len(qol_country)):
        lags = qol_country[t - p:t][::-1] 
        current_feats = feature_data_country[t]
        
        row = np.concatenate([lags, current_feats, dummy_country])
        X.append(row)
        y.append(qol_country[t])


X = np.array(X)
y = np.array(y)

# adding a bias column
Xnew = np.hstack([np.ones((X.shape[0], 1)), X])

# performing linear regression
XtXinv = np.linalg.inv(np.matmul(Xnew.T, Xnew))
m = np.matmul(XtXinv, np.matmul(Xnew.T, y))

print(m)




    
    
