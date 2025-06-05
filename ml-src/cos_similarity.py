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
input = np.array([1, 1, 1, 1])

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



def cosine_similarity(df, input_vector):
    """ returns a sorted dataframe of countries and their cosine similarity scores compared to the input vector.
        Args:
            df (pandas DataFrame): dataframe of all country's most recent data for all five features.
            input_vector (numpy.array): array of the input of the sliders in the order healthcare, education, safety, environment, infrastructure.
        Returns:
            sorted_df_scores (pandas DataFrame): a sorted dataframe of countries and their cosine similarity scores compared to the input vector.
    """
    cos_scores = []

    inv_sig_input = np.array(list(map(inv_sigmoid, input_vector)))

    for country in range(len(df)):
        temp_vector = np.array([df.iloc[country, 2], 
                            df.iloc[country, 3], 
                            df.iloc[country, 4], 
                            df.iloc[country, 5],])
        temp_vector = temp_vector/np.sum(temp_vector)
        cos_similarity = np.dot(inv_sig_input, temp_vector) / (np.linalg.norm(inv_sig_input) * np.linalg.norm(temp_vector))

        cos_scores.append(cos_similarity)

    dict_scores = {'Country_input': df.country,
                'similarity': cos_scores}

    df_scores = pd.DataFrame(dict_scores)

    sorted_df_scores = df_scores.sort_values('similarity', ascending = False)
    return sorted_df_scores

print(cosine_similarity(df, input))
