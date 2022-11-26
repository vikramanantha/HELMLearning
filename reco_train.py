# Vikram Anantha
# Apr 19 2021
# Recommendation Algorithm - Training
# HELM Learning
# Science Fair 2021

from helper_functions import *
# import make_df_v3
from helper_functions import *
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import math
import random
import pickle

import warnings
warnings.filterwarnings('ignore') 

cnx, cursor = start()
sql0 = 'SELECT id FROM classes'
cursor.execute(sql0)
num_classes = cursor.fetchall()[-1][0]
classes_that_are_legal = get_legal_classes()


def get_data():
    # make_df_v2.main()
    cnx, cursor = start()
    df = pd.read_csv("students_v4.2.csv")
    cols = []
    cursor.execute("SELECT id FROM classes")
    num_classes = cursor.fetchall()[-1][0]
    for j in range(3, num_classes+1):
        cols.append('took_class_%s' % j)
    stop(cnx, cursor)
    return cols, df

def train():
    cnx, cursor = start()
    cols, df = get_data()
    models = [None, None, None]
    sql0 = 'SELECT id FROM classes'
    cursor.execute(sql0)
    num_classes = cursor.fetchall()[-1][0]
    for i in range(3, num_classes+1): # this is for each model
        if i not in classes_that_are_legal:
            models.append(None)
            continue
        
        x_cols = df.loc[df['class'] == i]
        x = np.array(x_cols[cols])
        y = x_cols[['probs']]
        if (len(x) == 0):
            models.append(None)
            continue
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0, shuffle=True, test_size=0.25, train_size = 0.75)
        
        m_v1 = LogisticRegression()
        m_v1.fit(x, y)
        # 
        # if __name__ == "__main__":
        #     print("Model for Class: %s" % i)
        # 
        pickle.dump(m_v1, open("ClassModels/class_%s" % i, "wb"))
        models.append(m_v1)
    stop(cnx, cursor)
    # return models

def main():
    train()

if __name__ == "__main__":
    main()
