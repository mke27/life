# this model takes in input from the user in the form of sliders. 
# The user will slide 4 different 'factors'.
# Each country will be represented as a vector with the same factors.
# the cosine similarity score will be used to compare the given slider input to all the countries

import numpy as np
import pandas as pd


# reads in the CSV as df
df_all_years = pd.read_csv('datasets/preprocessed-datasets/all_data.csv')

# filters all data points that don't include a year of 2022
recent = (df_all_years.year == 2022)
df = df_all_years[recent]

# healthcare, education, safety, environment, infrastructure -> mock input
input = np.array([0, 0, 0, 0, 0]) # NOTE!!! REVERSE SIGMOID THE INPUTS FOR REAL INPUTS

def inv_sigmoid(value):
    """ returns the inverse sigmoid of the input. If the input is 0 or 1, rebounds the sigmoid to -3 or 3
        Args:
            value (int): value to be inversed sigmoided
        Returns:
            inv_sig (int): inverse sigmoid of input bounded between -3 and 3
    """
    if value == 1:
        value = .95
    elif value == 0:
        value = 0.05

    return np.log(value) - np.log(1-value)

inv_sig_input = np.array(list(map(inv_sigmoid, input)))

# makes a list of each country with that countries vector inside
# country_vector = [np.array(df.iloc[row, 0], 
#                            df.iloc[row, 1], 
#                            df.iloc[row, 2], 
#                            df.iloc[row, 3]) for row in range(len(df))]


cos_scores = []

for country in range(len(df)):
    temp_vector = np.array([df.iloc[country, 2], 
                           df.iloc[country, 3], 
                           df.iloc[country, 4], 
                           df.iloc[country, 5],
                           df.iloc[country, 6]])
    
    cos_similarity = np.dot(inv_sig_input, temp_vector) / (np.linalg.norm(inv_sig_input) * np.linalg.norm(temp_vector))

    cos_scores.append(cos_similarity)

dict_scores = {'Country_input': df.country,
            'similarity': cos_scores}

df_scores = pd.DataFrame(dict_scores)

sorted_df_scores = df_scores.sort_values('similarity', ascending = False)

print(sorted_df_scores)
