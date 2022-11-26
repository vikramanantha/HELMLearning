# Vikram Anantha
# Aug 2 2021
# Moving teacher data from website to database
# HELM Learning

import numpy
import mysql.connector
from mysql.connector import errorcode
from helper_functions import *
import pandas as pd


cnx, cursor = start()
filepath = "/Users/vikramanantha/Downloads/Management Responses - TEACHER INFO (9).csv"

# input()

### GETTING THE DATA



# read the CSV file into a DataFrame
df = pd.read_csv(filepath)
# 
# only take columns from the dataframe that match columns in the database table
numcols = 7
df2 = df[['Teacher Name', 'Teacher Description', 'Year of graduation', 'Email', 'Class 1', 'Class 2', 'Class 3', 'Is a Manager?', 'Community Service Hours']]

# if there are cells in the dataframe that are NaN, replace them with empty strings
df2 = df2.fillna('∑∑∑∑∑')
# print(df2)
# loop through all the rows in the dataframe and insert them into the table
# commit the data every 100 rows



### PUTTING THE DATA IN

sql1 = "INSERT INTO teachers (name, description, yog, classes, email, ismanager, community_service_hrs) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\");"
# 
# cursor.execute("DELETE FROM teachers")
# cursor.execute("DELETE FROM classes_to_teachers")
# cursor.execute("ALTER TABLE teachers AUTO_INCREMENT=1")

for i in df2.index:
    # print(df2.iloc[i].values.tolist())
    # quit()
    array = df2.iloc[i].values.astype(str).tolist()
    # array[0] = array[0][:-1]
    # print(array[0])
    # print("    ", end='')

    teach_info = array
    classes = teach_info[4]
    if (teach_info[5] != "∑∑∑∑∑"):
        classes += ", %s" % teach_info[5]
    if (teach_info[6] != "∑∑∑∑∑"):
        classes += ", %s" % teach_info[6]
    teach_info.remove(teach_info[4])
    teach_info.remove(teach_info[4])
    teach_info.remove(teach_info[4])
    teach_info.insert(3, classes)
    managerial_role = 0
    if ("Teacher" in teach_info[5]):
        managerial_role += 1
    if ("Manager" in teach_info[5]):
        managerial_role += 10
    if ("Hacker" in teach_info[5]):
        managerial_role += 100
    if ("Speaker" in teach_info[5]):
        managerial_role += 1000
    if ("Leader" in teach_info[5]):
        managerial_role += 10000
    teach_info[5] = managerial_role
    teach_info[2] = teach_info[2][0].upper() + teach_info[2][1:]

    teach_info[1] = teach_info[1].replace('"', '`')
    # print(teach_info)
    # input()

    cursor.execute("SELECT COUNT(id) FROM teachers WHERE name = '{}' AND email = '{}'".format(teach_info[0], teach_info[4]))
    numteach = cursor.fetchall()[0][0]
    if (numteach == 0):
        cursor.execute(sql1.format(*teach_info))
        print("%s has been added to the database!" % teach_info[0])
        try:
            upload_file_to_s3("helm-teacher-images", "/Users/vikramanantha/Downloads/Teacher Images/" + teach_info[0].lower().replace(" ", "-") + '-image.jpeg', teach_info[0].lower().replace(" ", "-") + "-image.jpeg")
        except:
            image_pathname = input("Praveeeeen!!!! Change the file name to be %s " % (teach_info[0].lower().replace(" ", "-") + "-image.jpeg"))
            upload_file_to_s3("helm-teacher-images", "/Users/vikramanantha/Downloads/Teacher Images/" + teach_info[0].lower().replace(" ", "-") + "-image.jpeg", teach_info[0].lower().replace(" ", "-") + "-image.jpeg")
        cursor.execute("UPDATE teachers SET image = '{}' WHERE name = '{}' AND email = '{}'".format(
            'https://helm-teacher-images.s3.amazonaws.com/' + teach_info[0].lower().replace(" ", "-") + "-image.jpeg",
            teach_info[0], teach_info[4]
            ))
    else:
        cursor.execute("SELECT classes FROM teachers WHERE name = '{}' AND email = '{}'".format(teach_info[0], teach_info[4]))
        cls = cursor.fetchall()[0][0];
        if (teach_info[3] != cls):
            cursor.execute("UPDATE teachers SET classes = '{}' WHERE name = '{}' AND email = '{}'".format(
                cls + ", " + teach_info[3],
                teach_info[0], teach_info[4],
            ))
        cursor.execute("UPDATE teachers SET description = \"{}\" WHERE name = '{}' AND email = '{}'".format(
            teach_info[1], teach_info[0], teach_info[4],
        ))

        cursor.execute("UPDATE teachers SET yog = '{}' WHERE name = '{}' AND email = '{}'".format(
            teach_info[2], teach_info[0], teach_info[4],
        ))

        cursor.execute("UPDATE teachers SET ismanager = '{}' WHERE name = '{}' AND email = '{}'".format(
            teach_info[5], teach_info[0], teach_info[4],
        ))

        cursor.execute("UPDATE teachers SET community_service_hrs = '{}' WHERE name = '{}' AND email = '{}'".format(
            teach_info[6], teach_info[0], teach_info[4],
        ))
        print("Updated %s's info" % (teach_info[0]))
        if (cls == teach_info[3]):
            print()
            continue
    # cnx.commit()
    cursor.execute("SELECT classes FROM teachers WHERE name = '{}' AND email = '{}'".format(teach_info[0], teach_info[4]))
    cls = cursor.fetchall()[0][0]
    print(cls)
    if (cls == "<none on file>"):
        print()
        continue
    
    print("Added these classes to the teacher:")
    for i in cls.split(", "):
        try:
            cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(i))
            class_id = cursor.fetchall()[0][0]
        except:
            newi = input("Praveeeeen!!!! What is the actual class name (hint, it's not %s):\n" % i) # jk praveen you're amazing
            cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(newi))
            class_id = cursor.fetchall()[0][0]
        cursor.execute("SELECT id FROM teachers WHERE name = '{}' AND email = '{}'".format(teach_info[0], teach_info[4]))
        teacher_id = cursor.fetchall()[0][0]
        cursor.execute("INSERT INTO classes_to_teachers (class_id, teacher_id) VALUES ('{}', '{}')".format(class_id, teacher_id))
        print("  %s >> %s" % (teacher_id, class_id))
    print()

# do a final commit
input("Commit? ")
cnx.commit()
# cursor.execute("SELECT * FROM teachers WHERE name = 'Ayan Nayak'")
# piano = cursor.fetchall()
# print(piano)
# close the cursor and database connection
cursor.close()
cnx.close()
