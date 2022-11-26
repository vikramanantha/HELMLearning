# Vikram Anantha
# Feb 6 2021
# Moving Tags from Google Sheets to SQL Database
# HELM Learning
# Science Fair 2021

import numpy
import mysql.connector
from mysql.connector import errorcode
from helper_functions import *
import pandas as pd


cnx = create_connection()
cursor = cnx.cursor(buffered=True)
filepath = "/Users/vikramanantha/Downloads/Management Responses - TAGGING CLASSES.csv"


sql1 = "INSERT INTO tags (tag) VALUES ('{}');"
sql2 = "INSERT INTO classes_to_tags (class_id, tag_id) VALUES ('{}', '{}');"
sql3 = "SELECT id FROM tags WHERE tag='{}'"
sql4 = "SELECT id FROM classes WHERE short_name='{}'"
# input()

### GETTING THE DATA



# read the CSV file into a DataFrame
df = pd.read_csv(filepath)
# 
# only take columns from the dataframe that match columns in the database table
df2 = df[['name', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5']]

# if there are cells in the dataframe that are NaN, replace them with empty strings
df2 = df2.fillna('XXX')
print(df2)
# loop through all the rows in the dataframe and insert them into the table
# commit the data every 100 rows



### PUTTING THE DATA IN



for i in df2.index:
    # print(df2.iloc[i].values.tolist())
    # quit()
    array = df2.iloc[i].values.astype(str).tolist()
    array[0] = array[0][:-1]
    print(array[0])
    print("    ", end='')
    for i in range(1, 6):
        if array[i] == "XXX":
            continue
        print(array[i] + ',  ', end="")
        cursor.execute(sql3.format(array[i]))
        tid = cursor.fetchall()

        cursor.execute(sql4.format(array[0]))
        cid = cursor.fetchall()[0][0]
        if len(tid) == 0:
            cursor.execute(sql1.format(array[i]))
            cursor.execute(sql3.format(array[i]))
            tid = cursor.fetchall()[0][0]
        else:
            tid = tid[0][0]
        cursor.execute(sql2.format(cid, tid))
    print()

cursor.execute("SELECT * FROM tags")
print(cursor.fetchall())
# do a final commit
input("Commit? ")
cnx.commit()

# close the cursor and database connection
cursor.close()
cnx.close()
