# Vikram Anantha
# Feb 16 2021
# Recommendation Algorithm - All
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


cursor = connect()
sql0 = 'SELECT id FROM classes'
cursor.execute(sql0)
num_classes = cursor.fetchall()[-1][0]

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
        if i == 40 or i == 46 or i == 45:
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
        if __name__ == "__main__":
            print("Model for Class: %s" % i)
        models.append(m_v1)
    stop(cnx, cursor)
    return models

def predict(fname, email, class_taken=""):
    cnx, cursor = start()
    sql0 = 'SELECT id FROM classes'
    cursor.execute(sql0)
    num_classes = cursor.fetchall()[-1][0] 
    cursor.execute("SELECT id FROM students WHERE Student_Name = '{}' and Email_Address = '{}'".format(fname, email))
    id = cursor.fetchall()[0][0]
    data = [0]*(num_classes-2)
    # cursor.execute("SELECT Grade FROM students WHERE id = '{}'".format(id))
    cursor.execute("SELECT class_id FROM classes_to_students WHERE student_id = '{}'".format(id))
    cids = cursor.fetchall()
    classes = list(set(np.reshape(cids, (1, len(cids)))[0]))

    tags4tags = get_tags_from_classes(classes)
    for i in classes:
        data[i-3] = 10
    for i in tags4tags:
        data[i[0]-3] = i[1]

    print(classes)
    models = train()
    predictions = []
    for m in models:
        if m == None:
            continue
        # print(list(m.predict_proba(np.array(data).reshape(1, -1))))
        pred = (int(list(m.predict_proba(np.array(data).reshape(1, -1)))[0][-1]*10000)/100)
        cool = [pred, models.index(m)]
        if __name__ == "__main__":
            print(cool)
        predictions.append(cool)
    predictions.sort()
    predictions.reverse()
    # print(predictions)
    recommended = []
    
    count = 0
    recommended_classes_number = 3
    random_classes_number = 1
    for i in predictions:
        if count == recommended_classes_number:
            break
        if i[1] not in recommended and i[1] not in classes:
            cursor.execute("SELECT short_name FROM classes WHERE id = '{}'".format(i[1]))
            class_name = cursor.fetchall()[0][0]
            # print(class_name, i[1])
            if class_name.lower() != class_taken.lower():
                recommended.append(class_name)
                count += 1
        # print(recommended)
    
    count = 0
    while count < random_classes_number:
        choice = random.choice(predictions)[1]
        if choice not in classes:
            cursor.execute("SELECT short_name FROM classes WHERE id = '{}'".format(choice))
            class_name = cursor.fetchall()[0][0]
            if class_name not in recommended and class_name != class_taken:
                recommended.append(class_name)
            count += 1
    # print(recommended)
    classes.sort()
    print(classes)
    cursor.execute("SELECT class_id FROM classes_to_students WHERE student_id = '{}'".format(id))
    sb = list(np.reshape(list(set(cursor.fetchall())), (1, -1))[0])
    sb.sort()
    print(sb)
    stop(cnx, cursor)
    return recommended

if __name__ == "__main__":  
    cnx, cursor = start()
    class_predicted = predict("Mark", "dasmartone3141@gmail.com")
    # fname = input("Name? ")
    # email = input("Email? ")
    # class_predicted = use(fname, email)
    print(class_predicted)
    stop(cnx, cursor)

