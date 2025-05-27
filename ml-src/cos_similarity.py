# this model takes in input from the user in the form of sliders. 
# The user will slide 4 different 'factors'.
# Each country will be represented as a vector with the same factors.
# the cosine similarity score will be used to compare the given slider input to all the countries

import numpy as np
import pandas as pd

# education, infrastructure, environment, safety
input = np.array([1, 0.5, 0.2, 0.1])

# makes a list of each country with that countries vector inside
country_vector = [np.array(df.iloc[row, 0], 
                           df.iloc[row, 1], 
                           df.iloc[row, 2], 
                           df.iloc[row, 3]) for row in range(len(df))]

cos_scores = []

for country in range(len(df)):
    temp_vector = np.array(df.iloc[country, 0], 
                           df.iloc[country, 1], 
                           df.iloc[country, 2], 
                           df.iloc[country, 3])
    
    cos_similarity = np.dot(input, temp_vector) / (np.linalg.norm(input) * np.linalg.norm(temp_vector))

    cos_scores.append(cos_similarity)

dict_scores = {'Country_input': df.country,
            'similarity': cos_scores}

df_scores = pd.DataFrame(dict_scores)

sorted_df_scores = df_scores.sort_values('similarity', ascending = False)


