# Vikram Anantha
# Apr 18 2021
# Moving Feedback from Google Sheets to SQL Database
# HELM Learning
# Science Fair 2021

import numpy
import mysql.connector
from mysql.connector import errorcode
from helper_functions import *
import pandas as pd


cnx, cursor = start()
filepath = "/Users/vikramanantha/Downloads/Management Responses - SQLFeedback-5.csv"  ########## JFNKHELJBFIHKEJBSKFKAHJBFKHJFBEKHFKHEBKEHB ############

# input()

### GETTING THE DATA



# read the CSV file into a DataFrame
df = pd.read_csv(filepath)
# 
# only take columns from the dataframe that match columns in the database table
numcols = 7
df2 = df[['timestamp', 'student_id', 'class_id', 'like_the_content', 'hard_the_content', 'fast_the_content', 'comment']]

# if there are cells in the dataframe that are NaN, replace them with empty strings
df2 = df2.fillna('†††')
print(df2)
# loop through all the rows in the dataframe and insert them into the table
# commit the data every 100 rows



### PUTTING THE DATA IN

sql1 = "INSERT INTO feedbackresponses (timestamp, student_id, class_id, like_the_content, hard_the_content, fast_the_content, comment) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');"

sql4 = 'SELECT id FROM classes WHERE name="{}"'

for i in df2.index:
    # print(df2.iloc[i].values.tolist())
    # quit()
    array = df2.iloc[i].values.astype(str).tolist()
    array[0] = array[0][:-1]
    # print(array[0])
    # print("    ", end='')

    cursor.execute(sql4.format(array[2]))
    try:
        cid = cursor.fetchall()[0][0]
    except:
        # print(array[i][0])
        print("This dumbo said %s" % array[2])
        the_real_class_name = input("############## What did they mean? ################### ")
        cursor.execute("SELECT id FROM classes WHERE name='{}'".format(the_real_class_name))
        cid = cursor.fetchall()[0][0]
    sid = get_id_from_student(fname=array[1])

    for j in range(0, numcols):
        if array[j] == "†††":
            continue
        # print(array[i] + ',  ', end="")

        if (j == 1):
            array[j] = sid
        if (j == 2):
            array[j] = cid
    cursor.execute(sql1.format(*array))
    cursor.execute("SELECT student_id, class_id, timestamp FROM feedbackresponses WHERE timestamp = '{}'".format(array[0]))
    print(i, cursor.fetchall()[0])
    print()

cursor.execute("SELECT * FROM tags")
print(cursor.fetchall())
# do a final commit
input("Commit? ")
cnx.commit()

# close the cursor and database connection
cursor.close()
cnx.close()
