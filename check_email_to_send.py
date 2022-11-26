#!/home/myuser/bin/python

# Vikram Anantha
# Dec 28 2020
# Check email to send
# HELM Learning

from helper_functions import *
import sys; sys.path.append('/home/ec2-user/anaconda3/lib/python3.8/site-packages/mysql')
import timed_email_sending as tes
import datetime
import pytz
import random
cnx, cursor = start()
est = pytz.timezone('America/New_York') 
# today = datetime.date.today()
rn = datetime.datetime.now(est)
today = datetime.datetime.strptime(rn.strftime("%Y-%m-%d"), "%Y-%m-%d")
sql = "SELECT short_name FROM classes WHERE startdate = '{}' AND starttime = '{}'"
sql22222 = "SELECT short_name FROM classes WHERE enddate = '{}' AND endtime = '{}'"
sql55 = "SELECT short_name FROM classes WHERE startdate = '{}' AND endtime = '{}'"
# today = datetime.date(2021, 5, 18)
# rn = datetime.datetime(1010, 1, 11, 18, 00, 48, 698821)



# ---------------------------------------------ER2
day = today.strftime("%Y-%m-%d")
time = rn.strftime("%H:%M")

cursor.execute(sql.format(day, time))
classes_er2 = cursor.fetchall()

for i in classes_er2:
    print(i[0])
    tes.er2(class_name = i[0], cursor=cursor)
    print('-------')



# ---------------------------------------------ER1
day = (today + datetime.timedelta(days=4)).strftime("%Y-%m-%d")
time = rn.strftime("%H:%M")

cursor.execute(sql.format(day, time))
classes_er1 = cursor.fetchall()

for i in classes_er1:
    print(i[0])
    tes.er1(class_name = i[0], cursor=cursor)
    print('-------')



# ---------------------------------------------E1
day = (today + datetime.timedelta(days=9)).strftime("%Y-%m-%d")
time = rn.strftime("%H:%M")

cursor.execute(sql.format(day, time))
classes_e1 = cursor.fetchall()

for i in classes_e1:
    print(i[0])
    tes.e1(class_name = i[0], cursor=cursor)
    print('-------')



# ---------------------------------------------E4
day = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
time = rn.strftime("%H:%M")
cursor.execute(sql22222.format(day, time))
classes_e4 = cursor.fetchall()

for i in classes_e4:
    print(i[0])
    tes.e4(class_name = i[0], cursor=cursor)
    print('-------')

# # ---------------------------------------------ET2-LOGISTICS
# day = (today + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
# time = rn.strftime("%H:%M")

# cursor.execute(sql.format(day, time)) 
# classes_et = cursor.fetchall()

# for i in classes_et:
#     print(i[0])
#     tes.et2_logistics(class_name = i[0], cursor=cursor)
#     print('-------')

# # ---------------------------------------------ET2-SHARING
# day = (today + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
# time = rn.strftime("%H:%M")

# cursor.execute(sql.format(day, time)) 
# classes_et = cursor.fetchall()

# for i in classes_et:
#     print(i[0])
#     tes.et2_sharing(class_name = i[0], cursor=cursor)
#     print('-------')

# ---------------------------------------------ET3-EMAILS
day = (today + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
time = rn.strftime("%H:%M")

cursor.execute(sql.format(day, time)) 
classes_et = cursor.fetchall()

for i in classes_et:
    print(i[0])
    tes.et3_emails(class_name = i[0], cursor=cursor)
    print('-------')

# ---------------------------------------------ET3-ZOOM
day = (today + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
time = rn.strftime("%H:%M")

cursor.execute(sql.format(day, time)) 
classes_et = cursor.fetchall()

for i in classes_et:
    print(i[0])
    tes.et3_zoom(class_name = i[0], cursor=cursor)
    print('-------')


# ---------------------------------------------E3
day = (today).strftime("%Y-%m-%d")
time = rn.strftime("%H:%M")

cursor.execute(sql55.format(day, time))
classes_e3 = cursor.fetchall()

for i in classes_e3:
    print(i[0])
    tes.e3(class_name = i[0], cursor=cursor)
    print('-------')


# ---------------------------------------------ET4-END
day = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
time = rn.strftime("%H:%M")
cursor.execute(sql22222.format(day, time))
classes_et4 = cursor.fetchall()

for i in classes_et4:
    print(i[0])
    tes.et4_end(class_name = i[0], cursor=cursor)
    print('-------')

stop(cnx, cursor)