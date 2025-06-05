"""
model01.py is an example of how to access model parameter values that you are storing
in the database and use them to make a prediction when a route associated with prediction is
accessed. 
"""
from backend.db_connection import db
import numpy as np
import pandas as pd
import logging

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

    for factor in range(len(input_vector)):
       input_vector[factor] = input_vector[factor]/np.sum(input_vector)

    inv_sig_input = np.array(list(map(inv_sigmoid, input_vector)))

    current_app.logger.info(f"sigmoided vector = {inv_sig_input}, the type is {type(df)}")

    for country in range(len(df)):
        temp_vector = np.array([df.iloc[country, 1],
                            df.iloc[country, 2],
                            df.iloc[country, 3],
                            df.iloc[country, 4]])
        #temp_vector = temp_vector/np.sum(temp_vector)
        cos_similarity = np.dot(inv_sig_input, temp_vector) / (np.linalg.norm(inv_sig_input) * np.linalg.norm(temp_vector))

        cos_scores.append(cos_similarity)

    dict_scores = {'Country_input': df['country_name'],
                'similarity': cos_scores}

    df_scores = pd.DataFrame(dict_scores)

    sorted_df_scores = df_scores.sort_values('similarity', ascending = False)
    return sorted_df_scores


from flask import current_app

def train():
  """
  You could have a function that performs training from scratch as well as testing (see below).
  It could be activated from a route for an "administrator role" or something similar. 
  """
  return 'Training the model'

def test():
  return 'Testing the model'

def predict(health_score, education_score, safety_score, environment_score):
  """
  Retreives model parameters from the database and uses them for real-time prediction
  """
  # get a database cursor 
  cursor = db.get_db().cursor()
  # get the model params from the database
  query = 'SELECT country_name, health_score, education_score, safety_score, environment_score FROM ML_Score WHERE score_year = 2022'
  cursor.execute(query)
  return_val = cursor.fetchall()



  df = pd.DataFrame.from_dict(return_val)

  current_app.logger.info(f"Tfetch = {df}, the type is {type(df)}")
  #put the score between 0 and 1
  vector = np.array([health_score, education_score, safety_score, environment_score])/100

  current_app.logger.info(f"input vector = {vector}, the type is {type(vector)}")

  similarity_table = cosine_similarity(df, vector)

  return similarity_table