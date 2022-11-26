# Vikram Anantha
# Sept 22 2020
# Starting a class
# HELM Learning

def gettime(starttime, endtime):
    if (starttime == None):
        return ['TBD', 'TBD']
    stime = str(starttime).split(":")
    etime = str(endtime).split(":")
    if (int(stime[0]) >= 12):
        startam = "pm"
        if (int(stime[0]) > 12):
            stime[0] = int(stime[0]) - 12
    else:
        startam = "am"
    if (int(etime[0]) >= 12):
        endam = "pm"
        if (int(etime[0]) > 12):
            etime[0] = int(etime[0]) - 12
    else:
        endam = "am"
    time_est = str(stime[0]) + ":" + str(stime[1]) + startam + " - " + str(etime[0]) + ":" + str(etime[1]) + endam
    stime[0] = int(str(starttime).split(":")[0]) - 1
    etime[0] = int(str(endtime).split(":")[0]) - 1

    if (int(stime[0]) >= 12):
        startam = "pm"
        stime[0] = int(stime[0]) - 12
    else:
        startam = "am"
    if (int(etime[0]) >= 12):
        endam = "pm"
        etime[0] = int(etime[0]) - 12
    else:
        endam = "am"

    time_cst = str(stime[0]) + ":" + str(stime[1]) + startam + " - " + str(etime[0]) + ":" + str(etime[1]) + endam
    return [time_est, time_cst]


def getdate(startdate, enddate):
    months = {
        1: "Jan",
        2: "Feb",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "Aug",
        9: "Sept",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    if (startdate == None):
        return ['TBD', 'TBD']
    sdate = str(startdate).split("-")
    edate = str(enddate).split("-")
    start_date = months[int(sdate[1])] + ' ' + sdate[2] + ', ' + sdate[0]
    end_date = months[int(edate[1])] + ' ' + edate[2] + ', ' + edate[0]
    return [start_date, end_date]

# def send(student_fname, email, pemail, list_of_content):
#     port = 465
#     sender = "helmlearning2020@gmail.com"
#     password = "h3lml3arning"
    
#     message = MIMEMultipart("alternative")
#     message["Subject"] = subject.format(list_of_content[0])
#     message["From"] = "HELM Learning"
#     message["To"] = email
#     content = """
#     Hi {},
#     This is a reminder that the {} class is starting now. In case you missed it, here are the details

#     This class starts at {} EST - {} EST

#     This class is happening today ({}, {}).

#     Here is the zoom link: <a href="{}">{}</a>. """



#     html = content.format(
#         student_fname, 
#         list_of_content[0], 
#         list_of_content[1], 
#         list_of_content[2], 
#         list_of_content[3])
#     print(html)
#     part2 = MIMEText(html, "html")
#     message.attach(part2)
#     context = ssl.create_default_context()
    

#     with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#         server.login(sender, password)
#         try:
#             #input("send?")
#             server.sendmail(sender, email, message.as_string())
#             server.sendmail(sender, pemail, message.as_string())
#             print("  Sent!")
#         except:
#             print()

import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
config = {
    'user': 'helmlearning',
    'password': 'H3lml3arning',
    'host': '127.0.0.1', #52.21.172.100:22
    'port': '3306',
    'database': 'HELM_Database'
}

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
db = "HELM_Database"
cnx = create_connection()
cursor = cnx.cursor(buffered=True)
class_name = input("class? ").lower()
class_name = class_name[0].upper() + class_name[1:]

sql = 'SELECT id, final_student FROM classes WHERE short_name = "{}"'
sql2 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "{}" AND which = "1"'
sql3 = 'UPDATE classes SET final_student = "{}" WHERE short_name="{}"'
sql4 = 'UPDATE classes SET class_started = 1 WHERE short_name = "{}"'



cursor.execute(sql.format(class_name))
class_id_stuff = cursor.fetchall()[0]
class_id = class_id_stuff[0]
final_student = class_id_stuff[1]
if (final_student == "" or final_student == None):
    cursor.execute(sql2.format(class_id))
    timestamp = cursor.fetchall()[-1][0]
    print(timestamp)
    print(sql3.format(timestamp, class_name))
    cursor.execute(sql3.format(timestamp, class_name))
    input("Good?")

cursor.execute(sql4.format(class_name))

# cursor.execute(sql5.format(class_name))
# class_info = list(cursor.fetchall()[0])

# if (class_info[-2] == None):
#     class_info[-2] = "0000-00-00 00:00:00"

# cursor.execute(sql6.format(class_info[-1], class_info[-2], class_info[-3]))
# stud_ids = cursor.fetchall()

# emails = []
# for i in stud_ids:
#     cursor.execute(sql7.format(i[0]))
#     email_stuff = cursor.fetchall()[0]
#     emails.append(email_stuff)

# for j in emails:
#     print(i)
#     send(j[2], j[0], j[1], class_info)

cnx.commit()
cursor.close()
cnx.close()
