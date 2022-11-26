# Vikram Anantha
# Aug 6 2021
# Moving Students from Google Sheets to SQL Database
# HELM Learning

# utility to import Flint Subscriptions from Melissa's SmartSheet into the database for analysis

#db-schema: ex: HELM_Test_Database
#database: helmlearningdatabase-1

### IMPORTS AND SETUP


import numpy
import mysql.connector
from mysql.connector import errorcode

import pandas as pd

# set up port forwarding to your database via a terminal window
# ssh -L 3306:helmlearningdatabase-1.rds-account-id.us-east-1.rds.amazonaws.com:3306 ec2-user@52.21.172.100
#
# replace db-name, rds-account-id, ip-address-for-ec2 with your own account info

# set up database configuration (set the db-username, db-password and db-name for your database)
config = {
    'user': 'helmlearning',
    'password': 'H3lml3arning',
    'host': '127.0.0.1', #52.21.172.100:22
    'port': '3306',
    'database': 'HELM_Test_Database'
}



### ESTABLISHING CONNECTION



def create_connection():
    """
    Returns a database connection using mysql.connector
    """
    # open database connection
    global cnx
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise

# Export data to a CSV file, and then change the header row to match the column names in your database table (if they are different)
# Also, make sure that the date fields are formatted as "YYYY-MM-DD"

# change file path to match your CSV file location
filepath = "/Users/vikramanantha/Downloads/Class Responses - Arduino (1).csv"
db = "HELM_Database"
class_name = '"Fun with Arduino and Circuits"'
student_name_col = "Student_Name"
email_col = "Email_Address"
parent_col = "Parent_Email"

# get column names
cnx = create_connection()
cursor = cnx.cursor(buffered=True)

# get all the columns from your database table (replace db-schema and db-table to match your table)
#cursor.execute("show columns from HELM_Test_Database.exercise")
cursor.execute("show columns from {}.students".format(db))
arr = [column[0] for column in cursor.fetchall()]

arr = arr[1:]

# create parameter placeholders
params = "%s," * len(arr)
params = params[:-1]  # remove trailing comma

# generate the insert query SQL string
cols = ','.join(arr)
print(cols)
print(params)
sql = "INSERT IGNORE INTO {}.students ({})  VALUES ({});".format(db, cols, params)
print(sql)
sql2 = 'SELECT id FROM {}.students WHERE {} = {} AND {} = {}'
sql3 = 'SELECT id FROM {}.classes WHERE name = {};'
sql4 = 'INSERT INTO {}.classes_to_students (timestamp, class_id, student_id) VALUES ({}, {}, {})'


### GETTING THE DATA



# read the CSV file into a DataFrame
df = pd.read_csv(filepath)

# only take columns from the dataframe that match columns in the database table
df2 = df[arr]

# if there are cells in the dataframe that are NaN, replace them with empty strings
df2 = df2.fillna('')

# loop through all the rows in the dataframe and insert them into the table
# commit the data every 100 rows



### PUTTING THE DATA IN



for i in df2.index:
    timestamp = '"' + df2.iloc[i].values[0] + '"'
    name = '"' + df2.iloc[i].values[1] + '"'
    email = '"' + df2.iloc[i].values[2] + '"'
    parent_email = '"' + df2.iloc[i].values[3] + '"'
    print(df2.iloc[i].values.tolist())

    cursor.execute(sql, df2.iloc[i].values.astype(str).tolist())
    cursor.execute(sql2.format(db, student_name_col, name, email_col, email, parent_col, parent_email))
    #print(sql2.format(db, student_name_col, name, email_col, email))
    student_id = cursor.fetchall()[0][0]
    print(student_id)
    cursor.execute(sql3.format(db, class_name))
    #print(sql3.format(db, class_name))
    class_id = cursor.fetchall()[0][0]
    #print(class_id)
    #print("------------")
    cursor.execute(sql4.format(db, timestamp, class_id, student_id))

    if i % 100 == 99:
        print('row ', i)
        input("Commit?")
        cnx.commit()

# do a final commit
input("Commit?")
cnx.commit()

# close the cursor and database connection
cursor.close()
cnx.close()
