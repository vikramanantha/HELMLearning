# Vikram Anantha
# Oct 19 2020
# Adding classes to the database
# HELM Learning

#from timed_email_sending import getdate, gettime
import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from helper_functions import *

db = "HELM_Database"
cnx = create_connection()
cursor = cnx.cursor(buffered=True)
choice = input("Add or Edit or New Session? ").lower()
class_name = input("short_name? ").lower()
class_name = class_name[0].upper() + class_name[1:]
if (choice == "add"):
    n = input("class name? ")
    t = input("Teacher_name? ")
    e = input("email? ")
    d = input("description? ")
    st = input("starttime? ")
    et = input("endtime? ")
    sd = input("startdate? ")
    ed = input("enddate? ")
    da = input("day? ")
    a = input("ages? ")
    z = input("zoom? ")
    sc = input("student_cap? ")
    cs = input("class_started? ")
    sql = "INSERT INTO classes (name, short_name, teacher, email, description, starttime, endtime, startdate, enddate, day, ages, zoom, student_cap, class_started) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    sql = sql.format(n, class_name, t, e, d, st, et, sd, ed, da, a, z, sc, cs)
    cursor.execute(sql)
    print("The class has been added!")
    while True:
        more = input("Anything else? (type !help to see options)")
        if (more == "!help"):
            print("You can choose from")
            print("  e1_summary\n  e1_additionalwork\n  e3_briefdescription\n  e4_continuingfurther")
            continue
        if (more == "" or more == None):
            break
        res = input("What is the input for this? ")
        sql2 = "UPDATE classes SET {} = '{}' WHERE short_name = '{}'".format(more, res, class_name)
        cursor.execute(sql2)
        cnx.commit()
    cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(class_name))
    class_id = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO classes_to_students (class_id, student_id) VALUES ({}, 2272)".format(class_id))
elif (choice == "edit"):
    while True:
        more = input("What do you want to update? (type !help to see options) ")
        if (more == "!help"):
            print("You can choose from")
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'classes';")
            cols = cursor.fetchall();
            for i in range(len(cols)):
                print("   %s" % cols[i][0])
            continue
        if (more == "" or more == None):
            break
        sql3 = 'SELECT {} FROM classes WHERE short_name = "{}"'.format(more, class_name)

        cursor.execute(sql3)
        before = cursor.fetchall()[0][0]
        print("Current Value for this is \n%s" % before)

        res = input("What is the input for this? ")
        if res == "!same":
            continue
        sql2 = 'UPDATE classes SET {} = "{}" WHERE short_name = "{}"'.format(more, res, class_name)
        cursor.execute(sql3)
        before = cursor.fetchall()[0][0]
        cursor.execute(sql2)
        cursor.execute(sql3)
        after = cursor.fetchall()[0][0]

        print("Updated {} from \n{} \nto \n{}".format(more, before, after))
        cnx.commit()
    send_e1 = input("Should I send E1/E2? ")
    if (send_e1 == "yes"):
        import timed_email_sending
elif (choice.lower() in "new session"):
    st = input("starttime? ")
    et = input("endtime? ")
    sd = input("startdate? ")
    ed = input("enddate? ")
    da = input("day? ")
    sql2 = "UPDATE classes SET {} = '{}' WHERE short_name = '{}'"
    sql3 = "SELECT {} FROM classes WHERE short_name = '{}'"

    cursor.execute(sql2.format("starttime", st, class_name))
    cursor.execute(sql3.format("starttime", class_name))
    st = cursor.fetchall()[0][0]
    cursor.execute(sql2.format("endtime", et, class_name))
    cursor.execute(sql3.format("endtime", class_name))
    et = cursor.fetchall()[0][0]
    cursor.execute(sql2.format("startdate", sd, class_name))
    cursor.execute(sql3.format("startdate", class_name))
    sd = cursor.fetchall()[0][0]
    cursor.execute(sql2.format("enddate", ed, class_name))
    cursor.execute(sql3.format("enddate", class_name))
    ed = cursor.fetchall()[0][0]
    cursor.execute(sql2.format("day", da, class_name))
    cursor.execute(sql3.format("day", class_name))
    da = cursor.fetchall()[0][0]

    print("New session for the %s class is on %ss, %s - %s from %s - %s EST" % (class_name, da, sd, ed, st, et))

cnx.commit()
cursor.close()
cnx.close()
