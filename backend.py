#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Vikram Anantha
# Aug 22 2020
# All of the Backend code for HELM Learning
# HELM Learning 2020


"""
Created on Sat Aug 22 12:53:56 2020
Author: Vikram Anantha
"""


'''
Determinator key:
    D = 2 --> student is new and no interests, proceeed to page 2
    D = 3 --> student is returning but no interests, proceeed to page 3
    D = 4 --> student is returning and interests, proceeed to page 4
'''

# This is the code that runs all the operations for the first page of the webpage set
# The operations that are done are:
#   1. Read in info from the JSON file (name + email)
#   2. Read the credentials and store them. Parse through the SQL database to verify whether or not the credentials exist
#   3. Give back an output JSON that tells the webclient which page to proceed to
# print("HELLO1")
import json
import random
import smtplib as s
import ssl
import string
import time
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Sized
from xml.dom.minidom import parseString
# print("HELLO2")
import flask
import mysql.connector
#import MySQLdb
import numpy
import pandas as pd
from flask import jsonify, make_response, request, send_from_directory
from flask_cors import CORS
from mysql.connector import errorcode
import helper_functions as hf
import make_df_v4
# from OpenSSL import SSL
# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')  
import reco_predict as reco
import reco_train
import timed_email_sending as tes
from pprint import pprint
# from flask import Flask, request, send_from_directory
app = flask.Flask(__name__, static_folder='static')  
app.config["DEBUG"] = True
CORS(app, resources = {r"/api/v1/*": {"origins": "*"}})
#print("Alloo")
config = {
    'user': '[SECRET]',
    'password': '[SECRET]',
    'host': '[SECRET]', #52.21.172.100:22
    'port': '[SECRET]',
    'database': '[SECRET]'
}

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
    start_date = months[int(sdate[1])] + ' ' + sdate[2] + ' ' + sdate[0]
    end_date = months[int(edate[1])] + ' ' + edate[2] + ' ' + edate[0]
    return [start_date, end_date]

@app.route('/api/v1/resources/train_alg', methods=['GET'])
def train_reco_alg():
    reco_train.main()
    make_df_v4.main()
    return jsonify(['0'])


def encode(x): # 2272 ==> df-gb-sdsaasd-sd
    x = str(x)
    y = ""
    for i in x:
        for j in range(int(i)):
            y += random.choice(string.ascii_letters)
        y += "-"
    y = y[:-1]
    return y

def decode(y): # df-gb-sdsaasd-sd ==> 2272
    ys = y.split('-')
    x = ""
    for i in ys:
        x += str(len(i))
    x = int(x)
    # print(x)
    return x

@app.route('/api/v1/resources/get_id', methods=["GET"])
def get_student_id(fname=None, email=None, id=None, status=0):
    # status 0: being called by js
    # status 1: being called to get id
    # status 2: being called to get name
    og_status = -1
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    if status == 0:
        og_status = 0
        query_params = request.args
        id = query_params.get('id')
        fname = query_params.get('fname')
        email = query_params.get('email')
        if fname == "__" or fname == None:
            status = 2
        else:
            status = 1
    cnx.commit()
    if status == 1:
        cursor.execute("SELECT id FROM students WHERE Student_Name = '{}' AND (Email_Address = '{}' OR Parent_Email = '{}')".format(fname, email, email))
        id = cursor.fetchall()
        if len(id) != 0:
            id = id[0][0]
            id = encode(id)
        else:
            id = 'fname=' + fname.replace(' ', '$') + '&email=' + email
    elif status == 2:
        id = decode(id)
        # print(id)
        cursor.execute("SELECT Student_Name, Email_Address FROM students WHERE id = '{}'".format(id))
        student_info = cursor.fetchall()[0]
        fname = student_info[0]
        email = student_info[1]

    cnx.commit()
    cursor.close()
    cnx.close()

    if og_status == 0:
        return jsonify({
            "Student_fname": fname,
            "Student_email": email,
            "Student_id_hashed": id,
        })
    else:
        return {
            "Student_fname": fname,
            "Student_email": email,
            "Student_id_hashed": id,
        }

@app.route('/api/v1/resources/get_all_classes', methods=['GET'])
def select_class():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    sql = "SELECT name, short_name FROM classes ORDER BY short_name"
    cursor.execute(sql)
    classes = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify(classes)

@app.route('/api/v1/resources/exchange_cache', methods=['GET'])
def exchange_cache():
    cnx, cursor = hf.start()
    query_params = request.url.split("?")[1]
    # print(query_params) ##¬¬¬
    sbali = query_params.split("&")
    sbali = sbali[1:]
    toreturn = []
    for i in sbali:
        try:
            notimportant = int(i)
        except:
            toreturn.append(i)
            continue
        try:
            cursor.execute("SELECT item FROM cache WHERE id = '{}'".format(i))
            dathing = cursor.fetchall()[0][0]
            dathing = dathing.replace("„", "'")
            dathing = dathing.replace("`", '"')
            toreturn.append(dathing)
        except:
            print("\n\nSomeone tampered with the system!! :O\n\n")
    return jsonify(toreturn)

@app.route('/api/v1/resources/exchange_cache_newsession', methods=['GET'])
def exchange_cache_newsession():
    cnx, cursor = hf.start()
    query_params = request.url.split("?")[1]
    # print(query_params) ##¬¬¬
    sbali = query_params.split("&")
    toreturn = []
    for i in sbali:
        try:
            notimportant = int(i)
        except:
            toreturn.append(i)
            continue
        try:
            cursor.execute("SELECT item FROM cache WHERE id = '{}'".format(i))
            dathing = cursor.fetchall()[0][0]
            dathing = dathing.replace("„", "'")
            dathing = dathing.replace("`", '"')
            toreturn.append(dathing)
        except:
            print("\n\nSomeone tampered with the system!! :O\n\n")
    return jsonify(toreturn)

def sende0(subject, content, student_fname, email, pemail, class_name, teacher_name, teacher_email, description):
    sende0_v2(subject, content, student_fname, email, pemail, class_name, teacher_name, teacher_email, description)
    # port = 465
    # sender = "helmlearning2020@gmail.com"
    # password = "[secret]"
    # #input("Send?")
    # message = MIMEMultipart("alternative")
    # message["Subject"] = subject.format(class_name)
    # message["From"] = "HELM Learning"
    # message["To"] = email

    # html = content.format(student_fname, class_name, class_name, teacher_name, teacher_email, description, teacher_name, class_name)
    # #print(html)
    # #part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")
    # #message.attach(part1)
    # message.attach(part2)

    # context = ssl.create_default_context()

    # with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #     server.login(sender, password)
    #     server.sendmail(sender, email, message.as_string())
    #     server.sendmail(sender, pemail, message.as_string())
    #     print()
    #     print("%s, %s, %s" % (student_fname, email, pemail))
    #     print(class_name)
    #     print("Sent E0!")
    #     print()
    

def sende0_v2(subject, content, student_fname, email, pemail, class_name, teacher_name, teacher_email, description):
    #input("Send?")
    html = content.format("{}", class_name, class_name, teacher_name, teacher_email, description, teacher_name, class_name)
    
    hf.send_email_v2(
        subject.format(class_name),
        html,
        (email, student_fname),
        (pemail, student_fname)
    )

    print("\nSent E0!\n")
    

def sende1(subject, content, student_fname, email, pemail, class_name, teacher_name, brief_summary, time_est, time_cst, first_day, last_day, day, zoom_link, prerequisite, temail, skipclass=None):
    sende1_v2(subject, content, student_fname, email, pemail, class_name, teacher_name, brief_summary, time_est, time_cst, first_day, last_day, day, zoom_link, prerequisite, temail, skipclass=None)
    # weeklongdates = {
    #     "winter": "Dec 28 2020 - Jan 1 2021"
    # }
    # port = 465
    # sender = "helmlearning2020@gmail.com"
    # password = "[no peaking!!]"
    # #input("Send?")
    # message = MIMEMultipart("alternative")
    # message["Subject"] = subject.format(class_name)
    # message["From"] = "HELM Learning"
    # message["To"] = email
    # #print(zoom_link + "asdf")
    # #print(zoom_link == "")
    # #print(zoom_link == None)
    # if zoom_link == "":
    #     zoom_link = "TBD"
    # if day == "":
    #     day = "TBD"
    # if (" and " in teacher_name):
    #     content = content.replace("My name is", "We are")
    #     content = content.replace(", and I am excited to be your teacher!", ", and we are excited to be your teachers!")
    # if (skipclass != None):
    #     content = content.replace("5 Weeks, once per week)", "5 Weeks, once per week)<br><strong>{}</strong>".format(skipclass))
    # if(prerequisite == None):
    #     prerequisite = ""
    
    # if "weeklong" in day:
    #     content = content.replace("5 Weeks, once per week)", "5 days in one week, Mon-Fri)")
    #     html = content.format(student_fname, class_name, teacher_name, brief_summary, time_est, time_cst, "Monday", first_day, "Friday", last_day, zoom_link, zoom_link, prerequisite, teacher_name, temail, class_name)
    # else:
    #     if ", " in day:
    #         content = content.replace("5 Weeks, once per week)", "A couple weeks long on %s)" % day)
    #     html = content.format(student_fname, class_name, teacher_name, brief_summary, time_est, time_cst, day, first_day, day, last_day, zoom_link, zoom_link, prerequisite, teacher_name, temail, class_name)
    # #print(html)
    # #part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")
    # #message.attach(part1)
    # message.attach(part2)

    # context = ssl.create_default_context()

    # with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #     server.login(sender, password)
    #     server.sendmail(sender, email, message.as_string())
    #     server.sendmail(sender, pemail, message.as_string())
    #     print()
    #     print("%s, %s, %s" % (student_fname, email, pemail))
    #     print(class_name)
    #     print("Sent E1!")
    #     print()

def sende1_v2(subject, content, student_fname, email, pemail, class_name, teacher_name, brief_summary, time_est, time_cst, first_day, last_day, day, zoom_link, prerequisite, temail, skipclass=None):
    if zoom_link == "":
        zoom_link = "TBD"
    if day == "":
        day = "TBD"
    if (" and " in teacher_name):
        content = content.replace("My name is", "We are")
        content = content.replace(", and I am excited to be your teacher!", ", and we are excited to be your teachers!")
    if (skipclass != None):
        content = content.replace("5 Weeks, once per week)", "5 Weeks, once per week)<br><strong>{}</strong>".format(skipclass))
    if(prerequisite == None):
        prerequisite = ""
    
    if "weeklong" in day:
        content = content.replace("5 Weeks, once per week)", "5 days in one week, Mon-Fri)")
        html = content.format("{}", class_name, teacher_name, brief_summary, time_est, time_cst, "Monday", first_day, "Friday", last_day, zoom_link, zoom_link, prerequisite, teacher_name, temail, class_name)
    else:
        if ", " in day:
            content = content.replace("5 Weeks, once per week)", "A couple weeks long on %s)" % day)
        html = content.format("{}", class_name, teacher_name, brief_summary, time_est, time_cst, day, first_day, day, last_day, zoom_link, zoom_link, prerequisite, teacher_name, temail, class_name)


    hf.send_email_v2(
        subject.format(class_name),
        html,
        (email, student_fname),
        (pemail, student_fname)
    )

    print("\nSent E1!\n")

def sende2(subject, content, student_fname, email, pemail, class_name, teacher_name):
    sende2_v2(subject, content, student_fname, email, pemail, class_name, teacher_name)
    # port = 465
    # sender = "helmlearning2020@gmail.com"
    # password = "[sshhhh]"
    # #input("Send?")
    # message = MIMEMultipart("alternative")
    # message["Subject"] = subject.format(class_name)
    # message["From"] = "HELM Learning"
    # message["To"] = email

    # html = content.format(student_fname, class_name, teacher_name, class_name)
    # #print(html)
    # #part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")
    # #message.attach(part1)
    # message.attach(part2)

    # context = ssl.create_default_context()

    # with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #     server.login(sender, password)
    #     server.sendmail(sender, email, message.as_string())
    #     server.sendmail(sender, pemail, message.as_string())
    #     print()
    #     print("%s, %s, %s" % (student_fname, email, pemail))
    #     print(class_name)
    #     print("Sent E2!")
    #     print()

def sende2_v2(subject, content, student_fname, email, pemail, class_name, teacher_name):
    html = content.format('{}', class_name, teacher_name, class_name)

    hf.send_email_v2(
        subject.format(class_name),
        html,
        (email, student_fname),
        (pemail, student_fname)
    )

    print("\nSent E2!\n")

def connect_to_send(student_fname, email, class_name):
    db = "HELM_Database"
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    cursor.execute("show columns from {}.students".format(db))
    sql0 = 'SELECT class_started, day, student_cap, final_student, last_student FROM classes WHERE short_name = "%s"' % (class_name[0].upper() + class_name[1:])
    cursor.execute(sql0)
    le_stuffe = cursor.fetchall()[0]
    #print(le_stuffe)
    #print(zoom)
    sql = 'SELECT Email_Address, Parent_Email FROM students WHERE Student_Name = "%s" AND Email_Address = "%s"' % (student_fname, email)
    if (le_stuffe[0] == 0 and le_stuffe[1] != ''):
        if (le_stuffe[2] > -1 and le_stuffe[3] != None):
            sql2 = 'SELECT name, teacher FROM classes WHERE short_name = "%s";' % (class_name)
            email_name = "e2"
        elif (le_stuffe[2] == -1):
            email_name = "e1"
            sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork, email FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
        else:
            email_name = "e1"
            sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork, email FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
            sqlwl2 = 'SELECT id FROM classes WHERE short_name = "%s"' % class_name
            cursor.execute(sqlwl2)
            class_id = cursor.fetchall()[0][0]
            sqlwl1 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "%s" AND timestamp > "%s"' % (class_id, le_stuffe[4])
            cursor.execute(sqlwl1)
            wl_info = cursor.fetchall()
            #print(wl_info)
            if (len(wl_info) > le_stuffe[2]):
                
                # print(class_id)
                # sqlwl2 = 'SELECT id FROM students WHERE Student_Name = "%s"' % student_fname
                # cursor.execute(sqlwl2)
                # student_id = cursor.fetchall()[0][0]
                # print(student_id)
                # sqlwl3 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "%s" AND student_id = "%s"' % (class_id, student_id)
                # cursor.execute(sqlwl3)
                # timestamp_for_ssu = cursor.fetchall()
                # print(">>>" + str(timestamp_for_ssu))
                # timestamp_for_ssu = timestamp_for_ssu[len(timestamp_for_ssu)-1][0]
                # print(timestamp_for_ssu)
                # sqlwl4 = 'UPDATE classes SET final_student = "%s"' % timestamp_for_ssu
                # print(sqlwl4)
                # cursor.execute(sqlwl4)

                #print(">>>" + str(le_stuffe[2]))
                #print(">>>" + str(wl_info[le_stuffe[2]]))
                sqlwl3 = 'UPDATE classes SET final_student = "%s" WHERE short_name = "%s"' % (wl_info[le_stuffe[2]-1][0], class_name)
                #print(sqlwl3)
                cursor.execute(sqlwl3)
                sql2 = 'SELECT name, teacher FROM classes WHERE short_name = "%s";' % (class_name)
                email_name = "e2"
            
    else: 
        email_name = "e0"
        sql2 = 'SELECT name, teacher, email, description FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
    sql3 = 'SELECT subject, content FROM templates WHERE name="%s"' % email_name
    #print(sql2)
    #print(email_name)
    cursor.execute(sql)
    emails = cursor.fetchall()[0]
    email = emails[0]
    pemail = emails[1]
    cursor.execute(sql2)
    class_info = cursor.fetchall()[0]
    cursor.execute(sql3)
    stuff = cursor.fetchall()[0]
    subject = stuff[0]
    content = stuff[1]
    #print(class_info)
    #print(email)
    # if (le_stuffe[0] == 0 and le_stuffe[1] != ''):
    #     if (le_stuffe[2] > -1 and le_stuffe[3] != None):
    #         sende2(subject, content, student_fname, email, pemail, class_info[0], class_info[1])
    #     else:
    #         sende1(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], gettime(class_info[3], class_info[4])[0], gettime(class_info[3], class_info[4])[1], getdate(class_info[5], class_info[6])[0], getdate(class_info[5], class_info[6])[1], class_info[7], class_info[8], class_info[9])
    # else:
    #     sende0(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], class_info[3])

    if email_name == "e0":
        sende0(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], class_info[3])
    elif email_name == "e1":
        import datetime
        skipclass = None
        for i in skipping_weeks:
            if class_info[5] < datetime.date(i[0], i[1], i[2]) and class_info[6] > datetime.date(i[0], i[1], i[2]):
                skipclass = i[3]
        from datetime import datetime
        sende1(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], gettime(class_info[3], class_info[4])[0], gettime(class_info[3], class_info[4])[1], getdate(class_info[5], class_info[6])[0], getdate(class_info[5], class_info[6])[1], class_info[7], class_info[8], class_info[9], skipclass)

    else:
        sende2(subject, content, student_fname, email, pemail, class_info[0], class_info[1])

    cnx.commit()
    cursor.close()
    cnx.close()

    if (email_name == "e2"):
        return 1
    else:
        return 0

    #tutorial at https://realpython.com/python-send-email/


def connect_to_send_v2(student_fname, email, class_name, which):
    print(which)
    if (which == "async"): 
        send_async_email(student_fname, email, class_name)
        return
    cnx, cursor = hf.start()
    # cursor.execute("show columns from students")
    sql0 = 'SELECT class_started, day, student_cap, final_student, last_student FROM classes WHERE short_name = "%s"' % (class_name[0].upper() + class_name[1:])
    cursor.execute(sql0)
    le_stuffe = cursor.fetchall()[0]
    #print(le_stuffe)
    #print(zoom)
    sql = 'SELECT Email_Address, Parent_Email FROM students WHERE Student_Name = "%s" AND Email_Address = "%s"' % (student_fname, email)
    if (le_stuffe[0] == 0 and le_stuffe[1] != ''):
        if (le_stuffe[2] > -1 and le_stuffe[3] != None):
            sql2 = 'SELECT name, teacher FROM classes WHERE short_name = "%s";' % (class_name)
            email_name = "e2"
        elif (le_stuffe[2] == -1):
            email_name = "e1"
            sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork, email FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
        else:
            email_name = "e1"
            sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork, email FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
            sqlwl2 = 'SELECT id FROM classes WHERE short_name = "%s"' % class_name
            cursor.execute(sqlwl2)
            class_id = cursor.fetchall()[0][0]
            sqlwl1 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "%s" AND timestamp > "%s"' % (class_id, le_stuffe[4])
            cursor.execute(sqlwl1)
            wl_info = cursor.fetchall()
            #print(wl_info)
            if (len(wl_info) > le_stuffe[2]):
                
                # print(class_id)
                # sqlwl2 = 'SELECT id FROM students WHERE Student_Name = "%s"' % student_fname
                # cursor.execute(sqlwl2)
                # student_id = cursor.fetchall()[0][0]
                # print(student_id)
                # sqlwl3 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "%s" AND student_id = "%s"' % (class_id, student_id)
                # cursor.execute(sqlwl3)
                # timestamp_for_ssu = cursor.fetchall()
                # print(">>>" + str(timestamp_for_ssu))
                # timestamp_for_ssu = timestamp_for_ssu[len(timestamp_for_ssu)-1][0]
                # print(timestamp_for_ssu)
                # sqlwl4 = 'UPDATE classes SET final_student = "%s"' % timestamp_for_ssu
                # print(sqlwl4)
                # cursor.execute(sqlwl4)

                #print(">>>" + str(le_stuffe[2]))
                #print(">>>" + str(wl_info[le_stuffe[2]]))
                sqlwl3 = 'UPDATE classes SET final_student = "%s" WHERE short_name = "%s"' % (wl_info[le_stuffe[2]-1][0], class_name)
                #print(sqlwl3)
                cursor.execute(sqlwl3)
                sql2 = 'SELECT name, teacher FROM classes WHERE short_name = "%s";' % (class_name)
                email_name = "e2"
            
    else: 
        email_name = "e0"
        sql2 = 'SELECT name, teacher, email, description FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
    sql3 = 'SELECT subject, content FROM templates WHERE name="%s"' % email_name
    #print(sql2)
    #print(email_name)
    cursor.execute(sql)
    emails = cursor.fetchall()[0]
    email = emails[0]
    pemail = emails[1]
    cursor.execute(sql2)
    class_info = cursor.fetchall()[0]
    cursor.execute(sql3)
    stuff = cursor.fetchall()[0]
    subject = stuff[0]
    content = stuff[1]
    #print(class_info)
    #print(email)
    # if (le_stuffe[0] == 0 and le_stuffe[1] != ''):
    #     if (le_stuffe[2] > -1 and le_stuffe[3] != None):
    #         sende2(subject, content, student_fname, email, pemail, class_info[0], class_info[1])
    #     else:
    #         sende1(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], gettime(class_info[3], class_info[4])[0], gettime(class_info[3], class_info[4])[1], getdate(class_info[5], class_info[6])[0], getdate(class_info[5], class_info[6])[1], class_info[7], class_info[8], class_info[9])
    # else:
    #     sende0(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], class_info[3])

    if email_name == "e0":
        sende0(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], class_info[3])
    elif email_name == "e1":
        import datetime
        skipclass = None
        for i in skipping_weeks:
            if class_info[5] < datetime.date(i[0], i[1], i[2]) and class_info[6] > datetime.date(i[0], i[1], i[2]):
                skipclass = i[3]
        from datetime import datetime
        sende1(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], gettime(class_info[3], class_info[4])[0], gettime(class_info[3], class_info[4])[1], getdate(class_info[5], class_info[6])[0], getdate(class_info[5], class_info[6])[1], class_info[7], class_info[8], class_info[9], skipclass)

    else:
        sende2(subject, content, student_fname, email, pemail, class_info[0], class_info[1])

    cnx.commit()
    cursor.close()
    cnx.close()

    if (email_name == "e2"):
        return 1
    else:
        return 0

    #tutorial at https://realpython.com/python-send-email/

def send_async_email(fname, email, class_name):
    cnx, cursor = hf.start()
    cursor.execute("select subject, content from templates where name = 'es-async-1'")
    subject, content = cursor.fetchall()[0]
    cursor.execute('select short_name, async_link, async_desc, short_name, teacher, name from classes where short_name = "{}"'.format(class_name))
    loc = list(cursor.fetchall()[0])
    loc[3] = "signup.helmlearning.com?" + loc[3]
    content = content.format(fname, *loc)
    subject = subject.format(class_name[0].upper() + class_name[1:])
    cursor.execute('select Email_Address, Parent_Email from students where Student_Name = "%s" and Email_Address = "%s"' % (fname, email))
    email, pemail = cursor.fetchall()[0]

    hf.send_email(subject, content, email, pemail)
    hf.stop(cnx, cursor)


def get_data(fhandle):
    with open(fhandle, 'r') as j:
        contents = json.loads(j.read())
        print(contents)
    return contents

def create_connection():
    """
    Returns a database connection using mysql.connector
    """
    # open database connection
    global cnx
    try:
        cnx = mysql.connector.connect(**config)
        cnx.autocommit = True
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise


@app.route('/', methods=['GET'])
def basic_stuff():
    return "<h1>Welcome!!</h1>"

@app.route('/api/v1/resources/page0-to-next-page', methods=['GET'])
def page0_receive():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    id = query_params.get('id')
    #print(class_name)
    id = decode(id)
    sql = "SELECT * FROM students WHERE id='{}'".format(id)
    cursor.execute(sql)
    stufe = cursor.fetchall()
    is_correct = False
    if len(stufe) > 0:
        is_correct = True
    is_correct = False
    if len(stufe) > 0:
        data = {
            "is_correct": True
        }
    else:
        data = {
            "is_correct": False
        }
    
    cnx.commit()
    cursor.close()
    cnx.close()
    
    return jsonify(data)


@app.route('/api/v1/resources/page0-data', methods=['GET'])
def page0_data():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    id = query_params.get('id')
    class_name = query_params.get('class')
    class_name = class_name.replace('-', ' ')
    id = decode(id)
    sql = "SELECT * FROM students WHERE id='{}'".format(id)
    cursor.execute(sql)
    stufe = cursor.fetchall()
    if (len(stufe) == 0):
        return jsonify({})
    timestamp = datetime.now()
    cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(class_name))
    sb = cursor.fetchall()[0][0]
    sql = 'INSERT INTO classes_to_students_viewing (timestamp, class_id, student_id) VALUES("{}", "{}", "{}")'.format(timestamp, sb, id)
    cursor.execute(sql)

    print("\n\nPAGE0 DATA\n%s %s\n\n" % (id, class_name))

    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({})

@app.route('/api/v1/resources/page4-data', methods=['GET'])
def page4_data():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    try:
        id = query_params.get('id')
        class_name = query_params.get('class')
        ranking = query_params.get('ranking')
    except:
        return jsonify([0])
    class_name = class_name.replace('-', ' ')
    id = decode(id)
    time.sleep(2)
    sql = "SELECT * FROM students WHERE id='{}'".format(id)
    cursor.execute(sql)
    stufe = cursor.fetchall()
    if (len(stufe) == 0):
        return jsonify({})
    timestamp = datetime.now()
    cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(class_name))
    sb = cursor.fetchall()[0][0]
    sql = 'INSERT INTO classes_to_students_reco (timestamp, class_id, student_id, ranking) VALUES("{}", "{}", "{}", "{}")'.format(timestamp, sb, id, ranking)
    cursor.execute(sql) 
    hf.log(id, "Reco", "%s (rank: %s)" % (class_name, ranking)) 
    # print("\n\nPAGE4 DATA\n%s %s %s\n\n" % (id, class_name, ranking))
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({})  


@app.route('/api/v1/resources/page1-receive', methods=['GET'])
def page1_receive():
    try:
        cnx = create_connection()
        cursor = cnx.cursor(buffered=True)
        query_params = request.args
        try:
            fname = query_params.get('fname')
            fname = fname.replace('$', ' ')
            email = query_params.get('email')
            class_name = query_params.get('class')
            which = query_params.get('which')
        except:
            hf.stop(cnx, cursor)
            return jsonify({
                "output":0, 
            })
        class_name = class_name[0].upper() + class_name[1:]
        class_name = class_name.replace('-', ' ')
        #print(class_name)
        print()
        print('Name: ', fname)
        print('Email: ', email)
        print('Class: ', class_name)

        if (which != 'async'):
            if (fname == ''):
                hf.stop(cnx, cursor)
                return jsonify({
                    "output":5, 
                })
            elif (email == ''):
                hf.stop(cnx, cursor)
                return jsonify({
                    "output":6, 
                })

        cnx.commit()
        query = "SELECT * FROM students WHERE Student_Name = '{}' AND (Email_Address = '{}' OR Parent_Email = '{}')".format(fname, email, email)
        sql2 = "SELECT * FROM classes WHERE short_name = '{}'".format(class_name)
        determinator = 4
        cursor.execute(query)
        result = cursor.fetchall()
        # print(result)
        cursor.execute(sql2)
        classes = cursor.fetchall()
        some_random_data = get_student_id(fname=fname, email=email, status=1)
        
        if classes == []:
            hf.stop(cnx, cursor)
            return jsonify({
                "output":-1, 
                })

        if (which == 'async'):
            if result == []:
                hf.log("%s (%s)" % (fname, email), "New Student", "")
                cursor.execute('INSERT INTO students (Timestamp, Student_Name, Email_Address, City, State, Newsetter) VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format(datetime.now(), fname, email, "[M] %s" % hf.location_from_ip_address(), "", 1))
                some_random_data = get_student_id(fname=fname, email=email, status=1)
            data = {
                "output": 4,
                "fname": fname.replace(' ', '$'),
                "email": email,
                "Student_id_hashed": some_random_data["Student_id_hashed"],
            }
            hf.stop(cnx, cursor)
            return jsonify(data)

        

        if result == []:
            hf.log("%s (%s)" % (fname, email), "New Student", "")
            determinator = 2
            fname = fname.replace(' ', '$')
            data = {
                "output":determinator, 
                "fname": fname,
                "email": email,
                "Student_id_hashed": some_random_data["Student_id_hashed"],
                }
            hf.stop(cnx, cursor)
            return jsonify(data)
        else:
            data = {
                "output": determinator,
                "fname": result[0][2].replace(' ', '$'),
                "email": result[0][3],
                "pemail": result[0][4],
                "Student_id_hashed": some_random_data["Student_id_hashed"],
            }
            hf.stop(cnx, cursor)
            return jsonify(data)


        
    except Exception as e:
        print(e)
        return jsonify({"output":0})

@app.route('/api/v1/resources/page2-receive', methods=['GET'])
def page2():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    fname = query_params.get('fname')
    fname = fname.replace('$', ' ')
    email = query_params.get('email')
    pemail = query_params.get('pemail')
    age = query_params.get('age')
    town = query_params.get('town')
    town = town.replace('$', ' ')
    state = query_params.get('state')
    state = state.replace('$', ' ')
    hearabout = query_params.get('hearabout')
    hearabout = hearabout.replace('$', ' ')
    newsletter = query_params.get('newsletter')
    if (newsletter == "false"): news = 0
    else: news = 1
    timestamp = datetime.now()

    if (town == '' and state == ''):
        town = hf.location_from_ip_address()
        state = '[maybe]'


    #sql2 = 'INSERT INTO students (Timestamp, Student_Name, Email_Address, Parent_Email) VALUES("{}", "{}", "{}", "{}")'.format(timestamp, "Ria", "vikramanantha@gmail.com", "dasmartone3141@gmail.com")
    sql = 'INSERT INTO students (Timestamp, Student_Name, Email_Address, Parent_Email, City, State, Grade, Heard_about_us, Newsetter) VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(timestamp, fname, email, pemail, town, state, age, hearabout, news)
    #print("PAGE 2 IS WORKING %s" % sql)
    # print(sql)
    cnx.commit()
    cursor.execute(sql)

    cnx.commit()
    cursor.close()
    cnx.close()

    some_random_data = get_student_id(fname=fname, email=email, status=1)

    data = {
        "Student_id_hashed": some_random_data['Student_id_hashed'],
    }
    hf.log("%s" % (fname), "NewNew Student", "")
    return jsonify(data)

@app.route('/api/v1/resources/page4-receive', methods=['GET'])
def get_class_info():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    if (query_params.get('pemail') != None):
        timestamp = datetime.now()
        sql2 = 'INSERT INTO students (Timestamp, Student_Name, Email_Address, Parent_Email) VALUES("{}", "{}", "{}", "{}")'.format(timestamp, "Siddhi", "vikramanantha@gmail.com", "dasmartone3141@gmail.com")
        cursor.execute(sql2)
        return "<h1></h1>"
    try:
        short_name_of_class = query_params.get('class')
    except:
        return jsonify([0])
    short_class_name = short_name_of_class[0].upper() + short_name_of_class[1:]
    short_class_name = short_name_of_class.replace('-', ' ')
    sql = "SELECT name, description, teacher, email, starttime, endtime, startdate, enddate, zoom, day, class_started, ages FROM classes WHERE short_name = '{}'".format(short_class_name)
    # cursor.execute('set global max_allowed_packet=67108864')
    cursor.execute(sql)
    result = cursor.fetchall()
    if (len(result) == 0):
        return jsonify({'is_real': "false"})
    #print(result)
    class_name = result[0][0]
    description = result[0][1]
    teacher = result[0][2]
    email = result[0][3]
    starttime = result[0][4]
    endtime = result[0][5]
    startdate = result[0][6]
    enddate = result[0][7]
    zoom = result[0][8]
    day = result[0][9]
    class_started = result[0][10]
    ages = result[0][11]
    time = gettime(starttime, endtime)[0]
    date0 = getdate(startdate, enddate)[0]
    date1 = getdate(startdate, enddate)[1]
    cnx.commit()
    cursor.close()
    cnx.close()
    if (class_started == 1 or day == ""):
        #print("Hello")
        weekoutput = "TBD"
        zoom = "TBD"
    else:
        if "weeklong" in day:
            weekoutput = "Monday - Friday, " + date0 + " - " + date1
        else:
            weekoutput = day + ", " + date0 + " - " + day + ", " + date1
        import datetime
        for i in skipping_weeks:
            if startdate < datetime.date(i[0], i[1], i[2]) and enddate > datetime.date(i[0], i[1], i[2]):
                weekoutput += i[3]
        from datetime import datetime
    output = {
        "Name": class_name,
        "Description": description,
        "Teacher": teacher,
        "Email": email,
        "Time": time,
        "Week": weekoutput,
        "Zoom": zoom,
        "Age": ages,
        'is_real': "true"
    }
    return jsonify(output)

@app.route('/api/v1/resources/page4-receive-v2', methods=['GET'])
def get_class_info_v2():
    try:
        cnx = create_connection()
        cursor = cnx.cursor(buffered=True)
        query_params = request.args
        # if (query_params.get('pemail') != None):
        #     timestamp = datetime.now()
        #     sql2 = 'INSERT INTO students (Timestamp, Student_Name, Email_Address, Parent_Email) VALUES("{}", "{}", "{}", "{}")'.format(timestamp, "Siddhi", "vikramanantha@gmail.com", "dasmartone3141@gmail.com")
        #     cursor.execute(sql2)
        #     return "<h1></h1>"
        try:
            short_name_of_class = query_params.get('class')
            which = query_params.get('which')
        except:
            return jsonify([0])
        short_class_name = short_name_of_class[0].upper() + short_name_of_class[1:]
        short_class_name = short_name_of_class.replace('-', ' ')
        sql = "SELECT name, description, teacher, email, starttime, endtime, startdate, enddate, zoom, day, class_started, ages, async_link, async_desc FROM classes WHERE short_name = '{}'".format(short_class_name)
        # cursor.execute('set global max_allowed_packet=67108864')
        cursor.execute(sql)
        result = cursor.fetchall()
        if (len(result) == 0):
            return jsonify({'is_real': "false"})
        else:
            result = result[0];
        #print(result)
        class_name = result[0]
        description = result[1]
        teacher = result[2]
        email = result[3]
        starttime = result[4]
        endtime = result[5]
        startdate = result[6]
        enddate = result[7]
        zoom = result[8]
        day = result[9]
        class_started = result[10]
        ages = result[11]
        async_link = result[12]
        async_desc = result[13]
        time = gettime(starttime, endtime)[0]
        date0 = getdate(startdate, enddate)[0]
        date1 = getdate(startdate, enddate)[1]
        cnx.commit()
        cursor.close()
        cnx.close()

        in_session = False
        asyncs = False

        if (class_started != 1 and day != ""):
            in_session = True
        if (async_link != None and async_link != ""):
            asyncs = True

        hf.log("?", "Looking", class_name)

        sync_stuff = {
            "Name": class_name,
            "Le rest": "%s<br><br><i>Teacher:</i> <a href='mailto:%s'>%s</a><br><br><i>Recommended Grades:</i> %s" % (description, email, teacher, ages),
            "show": False
        }
        async_stuff = {
            "show": False
        }

        if in_session:
            if "weeklong" in day:
                weekoutput = "Monday - Friday, " + date0 + " - " + date1
            else:
                weekoutput = day + ", " + date0 + " - " + day + ", " + date1
            import datetime
            for i in skipping_weeks:
                if startdate < datetime.date(i[0], i[1], i[2]) and enddate > datetime.date(i[0], i[1], i[2]):
                    weekoutput += i[3]
            from datetime import datetime
            sync_stuff["Le rest"] += "<br><br><i>Class Time:</i> %s EST<br><br><i>Dates:</i> %s" % (time, weekoutput)
            sync_stuff["show"] = True
        else:
            sync_stuff["syncsync"] = "<br><br>This class is not running"

        if asyncs:
            async_stuff["show"] = True
            async_stuff["link"] = async_link
            async_stuff["desc"] = async_desc
            emb = async_link.split('/')[-1].split('?')[0]
            async_stuff["embedded link"] = "https://drive.google.com/embeddedfolderview?id=" + emb + "#list"
        
        show = ""

        if (sync_stuff["show"] and async_stuff["show"]):
            if (which == 'async'): show = 'async'
            elif(which == 'waitlist'): show = 'signup'
            elif(which == 'signup'): show = 'signup'
            else: show = 'signup'

        elif (sync_stuff["show"] and not async_stuff["show"]):
            if (which == 'async'): show = 'signup'
            elif(which == 'waitlist'): show = 'signup'
            elif(which == 'signup'): show = 'signup'
            else: show = 'signup'
        
        elif (not sync_stuff["show"] and async_stuff["show"]):
            if (which == 'async'): show = 'async'
            elif(which == 'waitlist'): show = 'waitlist'
            elif(which == 'signup'): show = 'async'
            else: show = 'async'
        
        elif (not sync_stuff["show"] and not async_stuff["show"]):
            if (which == 'async'): show = 'waitlist'
            elif(which == 'waitlist'): show = 'waitlist'
            elif(which == 'signup'): show = 'waitlist'
            else: show = 'waitlist'

        output = {
            "Sync": sync_stuff,
            "Async": async_stuff,
            "is_real": "true",
            "show": show,
        }
        return jsonify(output)
    except:
        return jsonify({"is_real": "false"})

cnx, cursor = hf.start()
cursor.execute("SELECT * FROM important_dates WHERE kind='1'")
skipping_weeks = cursor.fetchall()
hf.stop(cnx=cnx, cursor=cursor)

@app.route('/api/v1/resources/sendemail', methods=['GET'])
def to_send_email():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    try:
        short_name_of_class = query_params.get('class')
    except:
        return jsonify([0])
    short_name_of_class = short_name_of_class.replace("-", " ")
    
    

    sql_cid = 'SELECT id FROM classes WHERE short_name = "{}"'.format(short_name_of_class[0].upper() + short_name_of_class[1:])
    sql_check = 'SELECT COUNT(timestamp) FROM classes_to_students WHERE class_id = "{}" AND student_id = "{}" AND timestamp > "{}"'
    
    timestamp = datetime.now()
    sql_su = 'INSERT INTO classes_to_students (timestamp, class_id, student_id, which) VALUES("{}", "{}", "{}", "1")'
    
    sid = query_params.get('id')

    some_random_data = get_student_id(id=sid, status=2)
    student_fname = some_random_data["Student_fname"]
    email = some_random_data["Student_email"]
    sid = decode(sid)
    cursor.execute(sql_cid)
    cid = cursor.fetchall()[0][0]
    sb = 1
    output = 0
    cursor.execute(sql_check.format(cid, sid, timestamp - timedelta(5)))
    # print(sql_check.format(cid, sid, timestamp - timedelta(5)))
    num_of_sus = cursor.fetchall()[0][0]
    if num_of_sus == 0:
        cursor.execute(sql_su.format(timestamp,cid, sid))
        cnx.commit()
        print("\nSuccessfully signed %s up!" % student_fname)
        sb = 0
        output = connect_to_send(student_fname, email, short_name_of_class)
    #print(sid)
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({"output": output, "su_success": sb})

@app.route('/api/v1/resources/sendemail-v2', methods=['GET'])
def to_send_email_v2():
    try:
        cnx, cursor = hf.start()
        query_params = request.args
        try:
            short_name_of_class = query_params.get('class')
            short_name_of_which = query_params.get('which')
        except:
            return jsonify([0])
        short_name_of_class = short_name_of_class.replace("-", " ")

        if (short_name_of_which == "async"):
            which = 2
        else:
            which = 1
        
        
        sql_cid = 'SELECT id FROM classes WHERE short_name = "{}"'.format(short_name_of_class[0].upper() + short_name_of_class[1:])
        sql_check = 'SELECT COUNT(timestamp) FROM classes_to_students WHERE class_id = "{}" AND student_id = "{}" AND timestamp > "{}"'
        # print(sql_cid)
        timestamp = datetime.now()
        sql_su = 'INSERT INTO classes_to_students (timestamp, class_id, student_id, which) VALUES("{}", "{}", "{}", "{}")'
        
        sid = query_params.get('id')

        some_random_data = get_student_id(id=sid, status=2)
        student_fname = some_random_data["Student_fname"]
        email = some_random_data["Student_email"]
        sid = decode(sid)
        cursor.execute(sql_cid)
        cid = cursor.fetchall()[0][0]
        sb = 1
        output = 0
        cursor.execute(sql_check.format(cid, sid, timestamp - timedelta(5)))
        # print(sql_check.format(cid, sid, timestamp - timedelta(5)))
        num_of_sus = cursor.fetchall()[0][0]
        hf.log(student_fname, "Signed up", "%s (which=%s)" % (short_name_of_class, which))
        print("\nSigning %s up for %s (which=%s)!" % (student_fname, short_name_of_class, which))
        if which == 2:
            cursor.execute(sql_su.format(timestamp,cid, sid, which))
            hf.stop(cnx, cursor)
            return jsonify({"output": output, "su_success": 0})
        if num_of_sus == 0:
            cursor.execute(sql_su.format(timestamp,cid, sid, which))
            cnx.commit()
            
            sb = 0
            output = connect_to_send_v2(student_fname, email, short_name_of_class, short_name_of_which)
        
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"output": output, "su_success": sb})
    except:
        return jsonify({"output": 0})


@app.route('/api/v1/admin/getstudents', methods=['GET'])
def get_students():
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
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    username = '[SECRET]'
    password = '[SECRET]'
    un = query_params.get('un')
    pw = query_params.get('pw')
    if (username != un or password != pw):
        return "<h1>You're bad and you should feel bad about yourself</h1>"
    class_name = query_params.get('class_name')
    class_name = class_name.replace('-', ' ')
    other_params = query_params.get('filter')
    if class_name == "[[class name]]" or class_name == "all":
        string = "<h2>Click on a link below to see the students for your class</h2>"
        cursor.execute("SELECT short_name FROM classes")
        classes_names_short = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        string += "<p>You can choose from <br>"
        for j in classes_names_short:
            i = j[0].lower()
            string += '<a href=https://signup.helmlearning.com:5000/api/v1/admin/getstudents?un=hElMlEaRnInG&pw=mvemjsun&class_name=%s&filter=none>%s</a><br>' % (i.replace(' ', '-'), i[0].upper() + i[1:])
        return string
    sql = 'SELECT id, final_student, last_student FROM classes WHERE short_name = "%s"' % class_name
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261" AND which = "1"'
    sql3 = 'SELECT Student_Name, Email_Address, City, State, Grade, Heard_about_us FROM students WHERE id = "{}"'
    sql4 = 'SELECT COUNT(student_id) FROM classes_to_students WHERE class_id = "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261"'

    cursor.execute(sql)
    
    class_info = cursor.fetchall()[0]
    class_id = class_info[0]
    cursor.execute(sql2.format(class_id))
    student_ids = cursor.fetchall()
    cursor.execute(sql4.format(class_id))
    num_students = cursor.fetchall()[0][0]
    student_info = []
    count = 0
    if class_info[-1] == None:
        other_params= "none"
    #student_info.append("Total Students: %s" % num_students)
    curr_count = 0
    for i in student_ids:
        count += 1
        cursor.execute(sql3.format(i[0]))
        students = cursor.fetchall()[0]
        if (other_params == "current"):
            if (i[1] > class_info[-1]):
                if (class_info[-2] == None or i[1] <= class_info[-2]):
                    student_info.append({
                        "1. Name": students[0], 
                        "2. State": students[3], 
                        "3. Grade": students[4],
                        "4. How they know about HELM": students[5],
                        "5. When they signed up": str(i[1])
                    })
                    curr_count += 1
        else:
            student_info.append({
                "1. Name": students[0], 
                "2. State": students[3], 
                "3. Grade": students[4],
                "4. How they know about HELM": students[5],
                "5. When they signed up": str(i[1])
            }
        )
    #print(student_info)
    cnx.commit()
    cursor.close()
    cnx.close()
    return_string = ""
    
    if (other_params == "current"):
        return_string = '<h1>You are viewing: Students in your current session of the {} class</h1><h2>Click <a href="https://signup.helmlearning.com:5000/api/v1/admin/getstudents?un=hElMlEaRnInG&pw=mvemjsun&class_name={}&filter=none">here</a> to see all your students</h2>'.format(class_name, class_name)
    else:
        return_string = '<h1>You are viewing: All Students of the {} class</h1><h2>Click <a href="https://signup.helmlearning.com:5000/api/v1/admin/getstudents?un=hElMlEaRnInG&pw=mvemjsun&class_name={}&filter=current">here</a> to see students in your current session</h2>'.format(class_name, class_name)
    return_string += "Total Students: %s<br>" % num_students
    if (other_params == "current"):
        return_string += "Current Students: %s<br>" % curr_count
    for i in student_info:
        return_string += "<br>"
        for j in i:
            return_string += "%s: %s <br>" % (j, i[j])
    return return_string


@app.route('/api/v1/resources/admin_get_class_info', methods=['GET'])
def admin_class_info():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    try:
        short_name_of_class = query_params.get('class')
    except:
        return jsonify([0])
    short_class_name = short_name_of_class.replace('-', ' ')
    the_filter = query_params.get('filter')
    sql = "SELECT name, short_name,description, starttime, endtime, startdate, enddate, zoom, day, ages, sharing_mats, recordings FROM classes WHERE short_name = '{}'".format(short_class_name)
    cursor.execute(sql)
    try:
        result = cursor.fetchall()[0]
    except:
        return jsonify([0])
    class_name = result[0]
    short_name = result[1]
    description = result[2]
    starttime = result[3]
    endtime = result[4]
    startdate = result[5]
    enddate = result[6]
    zoom = result[7]
    day = result[8]
    age = result[9]
    sharing_mats = result[10]
    class_rec = result[11]

    time = gettime(starttime, endtime)[0] + " EST"
    date0 = getdate(startdate, enddate)[0]
    date1 = getdate(startdate, enddate)[1]
    if "weeklong" in day:
        weekoutput = "Monday - Friday, " + date0 + " - " + date1
    else:
        weekoutput = day + ", " + date0 + " - " + day + ", " + date1
    if startdate != None:
        import datetime
        for i in skipping_weeks:
            if startdate < datetime.date(i[0], i[1], i[2]) and enddate > datetime.date(i[0], i[1], i[2]):
                weekoutput += i[3]
        from datetime import datetime
    else:
        weekoutput = "No session is currently scheduled"
        time = "No session is currently scheduled"
    

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
    sql = 'SELECT id, final_student, last_student FROM classes WHERE short_name = "%s"' % short_class_name
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261" AND which = "1" ORDER BY timestamp'
    sql25 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261" AND which = "1" ORDER BY timestamp'
    sql3 = 'SELECT Student_Name, Email_Address, City, State, Grade, Heard_about_us FROM students WHERE id = "{}"'
    sql4 = 'SELECT COUNT(student_id) FROM classes_to_students WHERE class_id = "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261" AND which = "1"'
    sql45 = 'SELECT COUNT(student_id) FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261" AND which = "1"'
    cursor.execute(sql)
    
    class_info = list(cursor.fetchall()[0])
    if class_info[-1] == None or class_info[-1] == "":
        class_info[-1] = "0000-00-00 00:00:00"
    if class_info[-2] == None or class_info[-2] == "":
        class_info[-2] = "9999-99-99 99:99:99"
    class_id = class_info[0]
    if (the_filter == "all"):
        cursor.execute(sql2.format(class_id))
    else:
        cursor.execute(sql25.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    cursor.execute(sql4.format(class_id))
    num_students = cursor.fetchall()[0][0]
    cursor.execute(sql45.format(class_id, class_info[-1], class_info[-2]))
    num_students2 = cursor.fetchall()[0][0]
    
    student_info = []
    count = 0
    if (the_filter == "all"):
        student_info.append("Total Students: %s" % (num_students))
    else:
        student_info.append("Total Students: %s<br>Current Students: %s" % (num_students, num_students2))
    for i in student_ids:
        count += 1
        cursor.execute(sql3.format(i[0]))
        # print(sql3.format(i[0]))
        students = list(cursor.fetchall())
        if len(students) == 0:
            continue
        students = list(students[0])
        if students[2] == "" or students[2] == None:
            students[2] = "?"
        if students[4] == "" or students[4] == None:
            students[4] = "?"
        if students[5] == "" or students[5] == None:
            students[5] = "?"
        student_info.append([
            students[0], # name
            students[2] + ", " + students[3], # state
            students[4], # grade
            students[5], # know about us
            i[1].strftime("%b %d, %Y at %H:%M") # timestamp
        ])
    cnx.commit()
    cursor.close()
    cnx.close()



    output = {
        "Name": class_name,
        "Short name": short_name,
        "Description": description,
        "Time": time,
        "Week": weekoutput,
        "Age": age,
        "Zoom": zoom,
        "Sharing mats": sharing_mats,
        "Class recordings": class_rec,
        "Students": student_info
    }
    
    return jsonify(output)  

@app.route('/api/v1/resources/verifyteacher', methods=['GET'])
def verify_teacher():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    short_name_of_class = query_params.get('class')
    class_name = short_name_of_class.replace('-', ' ')
    email = query_params.get('email')
    pw = query_params.get('pw')

    ily = "SELECT email, teacher FROM classes WHERE short_name = '{}'"
    sb = "SELECT pw, cipher FROM verify"
    cursor.execute(ily.format(class_name))
    qwert = cursor.fetchall()
    class_email = qwert[0][0]
    teacher_name = qwert[0][1]
    print("\n%s is checking their class details!\n" % teacher_name)
    cursor.execute(sb)
    pws = list(cursor.fetchall())
    the_real_ones = []
    for i in pws:
        
        i = list(i)
        the_real_ones.append(hf.decrypt(i[0], i[1]))
    # print(email, pw, class_email, the_real_ones)
    # print(" and " in class_email and email in class_email.split(" and "))
    # print(email == the_real_ones[1])
    # print(email == class_email)
    # print((pw == the_real_ones[0]))
    cnx.commit()
    cursor.close()
    cnx.close()
    if (((" and " in class_email and email in class_email.split(" and ")) or (email == the_real_ones[1]) or (email == class_email)) and (pw == the_real_ones[0])):
        return jsonify(
            {"output": 1}
        )
    else:
        return jsonify(
            {"output": 0}
        )

@app.route('/api/v1/resources/admin_action_buttons', methods=["GET"])
def action_buttons():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    action = query_params.get('action')
    short_name_of_class = query_params.get('class')
    class_name = short_name_of_class.replace('-', ' ')
    if (action == "copy"):
        #sql = 'SELECT id, final_student, last_student FROM classes WHERE short_name = "%s"' % class_name
        import timed_email_sending
        emails = timed_email_sending.ge(class_name, cursor)
        toreturn = ""
        for i in emails:
            toreturn += i[0] + ", " + i[1] + ", "
        toreturn += "helmlearning2020@gmail.com"
        return jsonify([toreturn])
    else:
        import timed_email_sending as tes
        tes.er2(class_name, cursor)
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify(["hello"])

@app.route('/api/v1/resources/reco', methods=["GET"])
def run_reco():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    # fname = query_params.get('fname')
    # email = query_params.get('email')
    id = query_params.get('id')
    short_name_of_class = query_params.get('class')
    class_name = short_name_of_class.replace('-', ' ')

    some_random_data = get_student_id(id=id, status=2)
    fname = some_random_data["Student_fname"]
    email = some_random_data["Student_email"]

    cnx.commit()
    predictions = reco.predict(fname, email, class_name)
    print(("Next classes for %s: " + "%s "*len(predictions) + "\n") % (fname, *predictions))
    biglist = []
    for i in predictions:
        cursor.execute("SELECT short_name, description FROM classes WHERE short_name = '{}'".format(i))
        class_detail_stuff_meaning_name_and_description = list(cursor.fetchall()[0])
        cursor.execute("SELECT name, description FROM classes WHERE short_name = '{}'".format(i))
        full_class_name = cursor.fetchall()[0][0]
        class_detail_stuff_meaning_name_and_description[1] = "<i>" + full_class_name + "</i>: " + class_detail_stuff_meaning_name_and_description[1]
        class_detail_stuff_meaning_name_and_description[1] = class_detail_stuff_meaning_name_and_description[1][:150] + "..."
        # Just a btw, the height of the box is set in page4.html around line 216, currently set at 140px
        biglist.append(class_detail_stuff_meaning_name_and_description)
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify(biglist)

@app.route('/api/v1/resources/feedback', methods=['GET'])
def feedback():
    cnx, cursor = hf.start()
    query_params = request.args
    sid = query_params.get('id')
    class_name = query_params.get('class')
    class_name = class_name.replace('-', ' ')

    like = query_params.get('like')
    hard = query_params.get('hard')
    fast = query_params.get('fast')
    comment = query_params.get('comment')
    comment = comment.replace('$', ' ')
    timestamp = datetime.now()

    student_id = decode(sid)
    cursor.execute("SELECT id FROM classes WHERE short_name='{}'".format(class_name))
    try:
        class_id = cursor.fetchall()[0][0]
    except:
        class_id = 0
    sql = "INSERT INTO feedbackresponses (timestamp, student_id, class_id, like_the_content, hard_the_content, fast_the_content, comment) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    cursor.execute(sql.format(timestamp, student_id, class_id, like, hard, fast, comment))
    print("Successfully added Student %s's feedback for the %s class" % (student_id,class_name))

    hf.stop(cnx=cnx, cursor=cursor)
    return jsonify([0])

@app.route('/api/v1/resources/newsession_1', methods=['GET'])
def newsession_1():
    cnx, cursor = hf.start()
    query_params = request.args
    linfo = []
    linfo.append(query_params.get('fname'))
    linfo.append(query_params.get('classname'))
    linfo.append(query_params.get('class_duration'))
    linfo.append(query_params.get('new_class_time'))
    linfo.append(query_params.get('new_class_startdate'))
    linfo.append(query_params.get('new_class_enddate'))
    lindexes = []
    for i in range(len(linfo)):
        linfo[i] = linfo[i].replace("•", " ")
    for i in linfo:
        cursor.execute("INSERT INTO cache (item) VALUES ('{}')".format(i))
        cursor.execute("SELECT id FROM cache WHERE item = '{}'".format(i))
        lindexes.append(cursor.fetchall()[-1][0])
    try:
        cursor.execute("SELECT short_name, startdate, enddate, starttime, endtime FROM classes WHERE (startdate <= '{}' AND enddate >= '{}') OR (startdate <= '{}' AND enddate >= '{}')".format(
            linfo[4], linfo[4], linfo[5], linfo[5]
        ))
        
        lestuff = cursor.fetchall()
        desautreclasses = len(lestuff)
        for i in range(len(lestuff)):
            linfo.append("{} • {} - {}, {} - {} EST".format(*lestuff[i]))
    except:
        return jsonify(["2"])


    link = "teachers.helmlearning.com/newsession?{}&{}&{}&{}&{}&{}".format(*lindexes)
    email = """
    Yo yo yo<br>
    Est-ce que c'est work for HELM?<br>
    Teacher:    {}<br>
    Class:      {} (the class is {} mins long)<br>
    New time:   {}<br>
    Start date: {}<br>
    End Date:   {}<br>
    <br>
    Note: there are some other classes:<br>
    <br>
    """
    email += "{}<br>"*desautreclasses
    email += "<br>Accept the New Session here: <br><a href='{}'>{}</a><br>".format(link, link)
    hf.send_email(
        "{} • Here's a New Session!!".format(linfo[1]),
        email.format(*linfo),
        "vikramanantha@gmail.com",
        "helmlearning2020@gmail.com"
    )
    hf.stop(cnx, cursor)
    return jsonify(["0"])

@app.route('/api/v1/resources/newsession_2', methods=['GET'])
def newsession_2():
    cnx, cursor = hf.start()
    query_params = request.args
    linfo = []
    linfo.append(query_params.get('fname')) #               0
    linfo.append(query_params.get('classname')) #           1
    linfo.append(query_params.get('class_duration')) #      2 
    linfo.append(query_params.get('new_class_time')) #      3
    linfo.append(query_params.get('new_class_startdate')) # 4
    linfo.append(query_params.get('new_class_enddate')) #   5
    lindexes = []
    for i in range(len(linfo)):
        linfo[i] = linfo[i].replace("•", " ")

    startdate = linfo[4]
    startdate = startdate.replace("/", "-")
    enddate = linfo[5]
    enddate = enddate.replace("/", "-")
    starttime = linfo[3].split("-")[0]
    print(starttime)
    # print(datetime.strptime(starttime, "%H:%M"))
    try:
        starttime = linfo[3].split(" - ")[0]
        # datetime.strptime(starttime, "%H:%M")
    except:
        try:
            starttime = linfo[3].split("-")[0]
            print(starttime)
            # datetime.strptime(starttime, "%H:%M")
        except:
            return jsonify([1])
    try:
        endtime = linfo[3].split(" - ")[1]
        # datetime.strptime(endtime, "%H:%M")
    except:
        try:
            endtime = linfo[3].split("-")[1]
            # datetime.strptime(endtime, "%H:%M")
        except:
            return jsonify([1])
    if ";" in linfo[3]:
        return jsonify([1])

    
    day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    try:
        startday = day_name[datetime.strptime(linfo[4], '%Y-%m-%d').weekday()]
        endday = day_name[datetime.strptime(linfo[5], '%Y-%m-%d').weekday()]
    except:
        return jsonify([2])
    day = startday
    if startday == "Monday" and endday == "Friday":
        day = "weeklong"

    cursor.execute("UPDATE classes SET startdate='{}' WHERE short_name = '{}'".format(startdate, linfo[1]))
    cursor.execute("UPDATE classes SET enddate='{}' WHERE short_name = '{}'".format(enddate, linfo[1]))
    cursor.execute("UPDATE classes SET starttime='{}' WHERE short_name = '{}'".format(starttime, linfo[1]))
    cursor.execute("UPDATE classes SET endtime='{}' WHERE short_name = '{}'".format(endtime, linfo[1]))
    cursor.execute("UPDATE classes SET day='{}' WHERE short_name = '{}'".format(day, linfo[1])) 
    cnx.commit()
    zoomlink = hf.createMeeting(linfo[1])  
    cursor.execute("UPDATE classes SET zoom='{}' WHERE short_name = '{}'".format(zoomlink, linfo[1])) 
    

    cursor.execute("SELECT email FROM classes WHERE short_name = '{}'".format(linfo[1]))
    teach_email = cursor.fetchall()[0]
    if "and" in teach_email:
        teach_email = list(teach_email)
        teach_email = teach_email.split(" and ")
        
    hf.send_email(
        "A New Session Has Been Created For Your Class! | HELM Learning",
        "Hey {}, <br>A new session for your class has been created. You can check the details at <a href='teachers.helmlearning.com?{}'>teachers.helmlearning.com?{}</a> or at <a href='signup.helmlearning.com?{}'>signup.helmlearning.com?{}</a>".format(linfo[0], linfo[1], linfo[1], linfo[1], linfo[1]),
        *teach_email
    )
    hf.stop(cnx, cursor)
    return jsonify(["0"])

@app.route('/api/v1/resources/signup_to_be_teach_1', methods=['GET'])
def signup_to_be_teach_1():
    try:
        print("SIGN UP TO BE TEACH 1")
        cnx, cursor = hf.start()
        query_params = request.args
        linfo = []
        lautre_classes = []
        length = query_params.get('length')
        fnamepos = query_params.get('fnamepos')
        emailpos = query_params.get('emailpos')
        position = query_params.get('position')
        for i in range(int(length)):
            linfo.append(query_params.get(str(i)))
        if linfo[0] == "":
            return jsonify(['3'])
        lindexes = []
        for i in range(len(linfo)):
            linfo[i] = linfo[i].replace("º", " ")
        for i in linfo:
            i = i.replace('"', '`')
            i = i.replace("'", "„")
            cursor.execute('INSERT INTO cache (item) VALUES ("{}")'.format(i))
            cursor.execute('SELECT id FROM cache WHERE item = "{}"'.format(i))
            lindexes.append(cursor.fetchall()[-1][0])
        # try:
        #     cursor.execute("SELECT short_name, startdate, enddate, starttime, endtime FROM classes WHERE (startdate <= '{}' AND enddate >= '{}')".format(
        #         linfo[-1], linfo[-1]
        #     ))
            
        #     lestuff = cursor.fetchall()
        #     desautreclasses = len(lestuff)
        #     for i in range(len(lestuff)):
        #         lautre_classes.append("Stuff")
        # except:
        #     return jsonify(["0"]) # SHOULD RETURN 2
        lautre_classes.append("Stuff")
        # try:
        #     er = linfo[-3].split("; ")[0].split(":")
        # except:
        #     print(linfo[-3])
        #     return jsonify(["0"]) # SHOULD RETURN 1
        link = ("teachers.helmlearning.com/signup?" + position + "&" + "{}&"*(len(lindexes)))[:-1].format(*lindexes)
        # print(link)

        cache_name = 0
        cache_subject = 10
        cache_class_name = 9

        email = """
        What's going on my homies???<br>
        Il y a un noveau class pour le HELM<br>
        Teacher:    {}<br>
        Class:      {}<br>
        Subject:    {}<br>
        <br>
        Note: there are some other classes:<br>
        <br>
        """
        # email += "{}<br>"*desautreclasses
        email += "<br>Accept the New Class here: <br><a href='{}'>{}</a><br>".format(link, link)
        if (position != "teacher"):
            subject = "NUU " + position
        else:
            subject = "{} ¬ NUU CLASSS!!".format(linfo[cache_subject])
        hf.send_email(
            subject,
            email.format(linfo[cache_name], linfo[cache_class_name], linfo[cache_subject], *lautre_classes),
            "vikramanantha@gmail.com",
            "helmlearning2020@gmail.com"
        )

        subject2teacher = "Confirmation - Teacher sign up form | HELM Learning"
        email2teacher = """
        Hi {}!<br>
        Thank you so much for signing up to be a teacher! This is a confirmation that you have sent in your teacher sign up form.<br>
        <br>
        Someone from the HELM Management Team will review your application, and you will receive an email to confirm you are teaching this class.
        Once you have confirmed, you will receive several emails with information on on your class, how to share it to students, how to use zoom, etc.
        Make sure you keep this email address open!<br>
        <br>
        Thank you so much!
        <br>
        Vikram from <strong style='color: #642c94'>HELM Learning</strong><br>
        """
        hf.send_email(
            subject2teacher,
            email2teacher.format(linfo[int(fnamepos)]),
            linfo[int(emailpos)]
        )
        hf.stop(cnx, cursor)
        return jsonify(["0"])
    except Exception as e:
        print("\n\nALERT SOMETHING WENT WRONG\n\n")
        print(e)

        try:
            print("SIGN UP TO BE TEACH 1")
            cnx, cursor = hf.start()
            query_params = request.args
            linfo = []
            lautre_classes = []
            length = query_params.get('length')
            position = query_params.get('position')
            for i in range(int(length)):
                linfo.append(query_params.get(str(i)))
            if linfo[0] == "":
                return jsonify(['3'])
            lindexes = []
            for i in range(len(linfo)):
                linfo[i] = linfo[i].replace("º", " ")
            for i in linfo:
                i = i.replace('"', '`')
                i = i.replace("'", "„")
                cursor.execute('INSERT INTO cache (item) VALUES ("{}")'.format(i))
                cursor.execute('SELECT id FROM cache WHERE item = "{}"'.format(i))
                lindexes.append(cursor.fetchall()[-1][0])
            # try:
            #     cursor.execute("SELECT short_name, startdate, enddate, starttime, endtime FROM classes WHERE (startdate <= '{}' AND enddate >= '{}')".format(
            #         linfo[-1], linfo[-1]
            #     ))
                
            #     lestuff = cursor.fetchall()
            #     desautreclasses = len(lestuff)
            #     for i in range(len(lestuff)):
            #         lautre_classes.append("Stuff")
            # except:
            #     return jsonify(["0"]) # SHOULD RETURN 2
            lautre_classes.append("Stuff")
            # try:
            #     er = linfo[-3].split("; ")[0].split(":")
            # except:
            #     print(linfo[-3])
            #     return jsonify(["0"]) # SHOULD RETURN 1
            link = ("teachers.helmlearning.com/signup?" + position + "&" + "{}&"*(len(lindexes)))[:-1].format(*lindexes)
            # print(link)

            cache_name = 0
            cache_subject = 10
            cache_class_name = 9

            email = """
            What's going on my homies???<br>
            Il y a un noveau class pour le HELM<br>
            Teacher:    {}<br>
            Class:      {}<br>
            Subject:    {}<br>
            <br>
            Note: there are some other classes:<br>
            <br>
            """
            # email += "{}<br>"*desautreclasses
            email += "<br>Accept the New Class here: <br><a href='{}'>{}</a><br>".format(link, link)
            if (position != "teacher"):
                subject = "NUU " + position
            else:
                subject = "{} ¬ NUU CLASSS!!".format(linfo[cache_subject])
            hf.send_email(
                subject,
                email.format(linfo[cache_name], linfo[cache_class_name], linfo[cache_subject], *lautre_classes),
                "vikramanantha@gmail.com",
                "helmlearning2020@gmail.com"
            )

            hf.stop(cnx, cursor)
            return jsonify(["0"])

        except Exception as e:
            print(e)
            return jsonify(['5'])

@app.route('/api/v1/resources/signup_to_be_teach_2', methods=['GET'])
def signup_to_be_teach_2():
    cnx, cursor = hf.start()
    query_params = request.args
    linfo = []
    lautre_classes = []
    length = query_params.get('length')
    position = query_params.get('position')
    for i in range(int(length)):
        linfo.append(query_params.get(str(i)).replace("º", " "))
    
    if position == "manager" or position == 'hacker':
        print("SELECT ismanager, name, email FROM teachers WHERE name = '{}' AND email = '{}'".format(linfo[0], linfo[1]))
        cursor.execute("SELECT ismanager, name, email FROM teachers WHERE name = '{}' AND email = '{}'".format(linfo[0], linfo[1]))
        bipp = list(cursor.fetchall()[0])
        if (position == "manager"): 
            bipp[0] = int(bipp[0])+10
        else:
            bipp[0] = int(bipp[0])+100
        cursor.execute("UPDATE teachers SET ismanager = {} WHERE name = '{}' AND email = '{}'".format(*bipp))
        hf.send_email("Welcome to the " + position + " team | HELM Learning", "Welcome!", bipp[2])
        hf.stop(cnx, cursor)
        return jsonify(["0"])

    ledetails = [
        "teacher", "email", "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie",
        "name", "short_name", "e1_summary", "description", "boogiewoogie", "boogiewoogie",
        "ages", "boogiewoogie", "starttime", "day", "startdate", "e1_additionalwork", "e4_continuingfurther"
    ]
    leteacherdetails = [
        "name", "email", "phnumber", "boogiewoogie", "yog", "description", "image", "boogiewoogie", "boogiewoogie",
        "boogiewoogie", "class", "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie",
        "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie", "boogiewoogie"
    ]
    # if (linfo[leteacherdetails.index("image")]):
        # return jsonify([4])
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tobeinthedb1 = []
    tobeinthedb2 = []
    new_class_short_name = ""
    for i in range(len(linfo)):
        linfo[i] = linfo[i].replace("º", " ")
    leteacherinfo = linfo.copy()
    if (position == "teacher"):
        for i in range(len(linfo)):
            print("%s\n%s\n" % (ledetails[i], linfo[i]))
            if ledetails[i] == "boogiewoogie":
                continue
            
            tobeinthedb1.append(ledetails[i])
            tobeinthedb2.append(linfo[i])
            if ledetails[i] == "short_name":
                new_class_short_name = linfo[i]
            if ledetails[i] == "day":
                tobeinthedb2[-1] = tobeinthedb2[-1][:-2]
            if ledetails[i] == "starttime":
                if (" - " not in linfo[i]):
                    return jsonify(['1'])
                try:
                    letimes = linfo[i].split(" - ")[1].split(":")
                    print(letimes[1])
                except:
                    print(">>>>%s" % linfo[i])
                    return jsonify(['1'])
                lestimes = linfo[i].split(" - ")
                starttime, endtime = lestimes[0], lestimes[1]
                tobeinthedb2[-1] = starttime
                tobeinthedb2.append(endtime)
                tobeinthedb1.append("endtime")
            if ledetails[i] == "startdate":
                # print(linfo[i], linfo[i+1])
                day = linfo[i-1][:-2]
                try:
                    sdl = linfo[i].split("-")
                    datetimething = datetime(int(sdl[0]), int(sdl[1]), int(sdl[2]))
                    if day == "weeklong":
                        enddate = (datetimething + timedelta(days=4)).strftime("%Y-%m-%d")
                        
                    else:
                        tobeinthedb2[-1] = (datetimething + timedelta(days=( days.index(day) ))).strftime("%Y-%m-%d")
                        linfo[i] = tobeinthedb2[-1]

                        enddate = (datetime(int(linfo[i].split("-")[0]), int(linfo[i].split("-")[1]), int(linfo[i].split("-")[2])) + timedelta(days=34)).strftime("%Y-%m-%d")
                        ### CHECK FOR BREAK WEEKS ###
                    tobeinthedb2.append(enddate)
                    tobeinthedb1.append("enddate")
                except:
                    return jsonify(['2'])
                
        ### SEE IF CLASS TIME CONFLICTS ###
        classday = tobeinthedb2[tobeinthedb1.index("day")]
        classstartdate = tobeinthedb2[tobeinthedb1.index("startdate")]
        classstarttime = datetime.strptime(tobeinthedb2[tobeinthedb1.index("starttime")] + " " + classstartdate, "%H:%M %Y-%m-%d")
        
        classendtime = datetime.strptime(tobeinthedb2[tobeinthedb1.index("endtime")] + " " + classstartdate, "%H:%M %Y-%m-%d")
        print(classday, classstartdate, classstarttime, classendtime)
        sqlsql = "select starttime, endtime from classes where day=\"%s\" and startdate = \"%s\" and ((endtime >= \"%s\" and endtime <= \"%s\") or (starttime >= \"%s\" and starttime <= \"%s\"))"
        sqlsql = sqlsql % (classday, classstartdate, classstarttime, classendtime, classstarttime, classendtime)
        print(sqlsql)
        cursor.execute(sqlsql)
        qwe = cursor.fetchall()
        print(qwe)
        if (len(qwe) > 0): return jsonify(['10'])
        # for iii in qwe:
        #     if (classendtime >= iii[0] and classendtime <= iii[1]) or (classstarttime >= iii[0] and classstarttime >= iii[1]):
        #         print(iii)
        #         return jsonify(['10'])
        
        
        print(tobeinthedb1)
        print(tobeinthedb2)
        for i in range(len(max(tobeinthedb1, tobeinthedb2))):
            print("%s:\n   %s" % (tobeinthedb1[i], tobeinthedb2[i]))
        try:
            cursor.execute(('INSERT INTO classes (' + ('{}, '*len(tobeinthedb1))[:-2] + ') VALUES (' + ('"{}", '*len(tobeinthedb1))[:-2] + ')').format(*tobeinthedb1, *tobeinthedb2))
            cnx.commit()
        except:
            cursor.execute("SELECT id from classes where short_name = '%s'" % new_class_short_name) # TO BE CHANGEDDDDDD TODO
            cid = cursor.fetchall()[0][0]
            # sql = "UPDATE classes set "
            # for i in range(len(tobeinthedb1)-2):
            #     sql += tobeinthedb1[i] + ' = "' + tobeinthedb2[i] + '" AND '
            # sql = sql[:-4]
            # sql += "WHERE id = %s" % cid
            # print()
            # cursor.execute(sql)


            tochange = ['description', 'startdate', 'enddate', 'starttime', 'endtime', 'teacher', 'email', 'day', 'ages', 'e1_summary', 'e1_additionalwork', 'e4_continuingfurther']
            # sql = 
            for i in tochange:
                if ('no chango' in tobeinthedb2[tobeinthedb1.index(i)]): 
                    continue
                sql = "UPDATE classes set " + i + ' = "' + tobeinthedb2[tobeinthedb1.index(i)] + '" WHERE id = %s' % cid
                cursor.execute(sql)
            # sql += 
            # print(sql)
            # cursor.execute(sql)
            cnx.commit()
            print()
            print("\nTHIS CLASS ALREADY EXISTS!\n")
            # cursor.execute("UPDATE classes SET display = '0' WHERE id = %s" % cid)
            # return jsonify(['3'])
    cursor.execute("UPDATE classes SET display = '0' WHERE short_name = '%s'" % new_class_short_name)
    dabee = []
    isteacheralr = hf.is_teacher_is_in_db(cursor, linfo[leteacherdetails.index('name')], linfo[leteacherdetails.index('email')])
    for i in range(len(leteacherinfo)):
        if leteacherdetails[i] == "boogiewoogie":
            continue
        
        dabee.append(leteacherinfo[i])
        if (leteacherdetails[i] == "class" and position == "helm-club"):
            dabee[-1] = "HELM Club Member"
        if (leteacherdetails[i] == "image" and not isteacheralr):
            if (leteacherinfo[i] == "" or leteacherinfo[i] == None):
                leteacherinfo[i] = "https://drive.google.com/file/d/1cSN7k1q0_DbNsOOo3fL8R6lH-Z2elh3R/view?usp=sharing"
            try:
                print("1. asdiufnaljnskf")
                error = hf.download_googledrive_image(leteacherinfo[i], "dumpsterfiles/" + leteacherinfo[leteacherdetails.index("name")].lower().replace(" ", "-") + "-image.jpeg")
                # MAKE THAT ^^^^
                print("2. asdiufnaljnskf")
                if error == 1:
                    
                    cursor.execute("DELETE FROM classes WHERE short_name = '{}'".format(leteacherinfo[leteacherdetails.index("class")]))
                    cnx.commit()
                    return jsonify(['4'])
            except:
                print("asliudfblaisdnfkjlkjasdnfkjasnf")
                cursor.execute("DELETE FROM classes WHERE short_name = '{}'".format(leteacherinfo[leteacherdetails.index("class")]))
                cnx.commit()
                return jsonify(['4'])
            hf.upload_file_to_s3('helm-teacher-images', "dumpsterfiles/" + leteacherinfo[leteacherdetails.index("name")].lower().replace(" ", "-") + "-image.jpeg", leteacherinfo[leteacherdetails.index("name")].lower().replace(" ", "-") + "-image.jpeg")
            dabee[-1] = 'https://helm-teacher-images.s3.amazonaws.com/' + leteacherinfo[leteacherdetails.index("name")].lower().replace(" ", "-") + "-image.jpeg"
    if (position == "teacher"): 
        dabee.append("1")
        dabee.append("0")
    elif (position == "helm-club"): 
        dabee.append("100000")
        dabee.append("1")
    elif (position == "speaker"): 
        dabee.append("1000")
        dabee.append("1")
    print(leteacherinfo)
    print(dabee)     
    
    teacher_id = hf.add_teacher_to_db(dabee)

    if (position == "teacher"):
        cursor.execute("SELECT teacher, name, starttime, endtime, startdate, enddate, description, e1_summary, e1_additionalwork, e4_continuingfurther, day FROM classes WHERE short_name = '{}'".format(new_class_short_name))
        #                         0      1        2         3         4         5          6           7               8                    9            10
        class_info = list(cursor.fetchall()[0])
        
        class_info[2] = str(class_info[2]) + " - " + str(class_info[3])
        if class_info[10] == "weeklong":
            day = "Mon-Fri"
        else:
            day = class_info[10] + "s"
        print(class_info)
        class_info[4] = day + ", " + str(class_info[4]) + " - " + str(class_info[5])
        class_info.remove(class_info[10])
        class_info.remove(class_info[5])
        class_info.remove(class_info[3])
        link = "teachers.helmlearning.com/confirm-teacher-signup.html?{}&buggle".format(new_class_short_name.replace(" ", '-'))
        email = """
        Hello {},<br>
        Welcome to HELM Learning! Thank you for signing up to be a teacher. I am Vikram, part of the HELM Management Team. Your class would be a great addition to HELM Learning. There are just a few things we want to confirm before we officially add the class to the website.<br>
        <br>
        Class Name: {}<br>
        Class Time: {}<br>
        Starting Week to Ending Week: {}<br>
        Description: {}<br>
        Short description: {}<br>
        Additional Materials: {}<br>
        Steps for continuing after the session: {}<br>
        <br>
        Can you confirm all of those details? Or is there anything you would want to change?<br>
        <br>
        One other detail that we are making sure all teachers know is their responsabilities as a teacher. They aren't much, but it shouldn't be taken lightly. 
        Every teacher must look out for emails from HELM Learning, as well as any texts that come your way. Teachers should also make sure they know when their class is, 
        and they have their own way of making sure they are on time for class, in addition to the HELM reminder emails. Please also make sure that if there is an issue, you communucate that to us.<br>
        <br>
        We have had a couple incidents in the past where teachers don't show to their own class, and we have been forced to to cancel the class after students were already waiting in the Zoom Room for 30 mins. 
        Try not to let it come to that.<br>
        If you have any issues with that, or you will be unable to teach your class, please let us know ASAP.<br>
        <br>
        Once you have read this email and confirm that you will be teaching this class, please click this link: <a href='{}'>{}</a>. If you would like to make any edits, respond back to this email and we will update the database.<br>
        <br>
        Once again, thank you for joining HELM. <br>
        <br>
        Best wishes,<br>
        <br>
        Vikram from <strong style='color: #642c94'>HELM Learning</strong><br>
        """
        cursor.execute("SELECT teacher, name, starttime, endtime, startdate, enddate, description, e1_summary, e1_additionalwork, e4_continuingfurther, day FROM classes WHERE short_name = '{}'".format(new_class_short_name))
        #                         0       1       2         3         4         5          6           7               8                    9            10
        class_info = list(cursor.fetchall()[0])
        class_info[2] = str(hf.td_dt(class_info[2], "time").strftime("%I-%M%p")) + " - " + str(hf.td_dt(class_info[3], "time").strftime("%I-%M%p"))
        if class_info[10] == "weeklong":
            day = "Mon-Fri"
        else:
            day = class_info[10] + "s"
        class_info[4] = day + ", " + class_info[4].strftime("%A, %b %d, %Y") + " - " + class_info[5].strftime("%A, %b %d, %Y")
        class_info.remove(class_info[10])
        class_info.remove(class_info[5])
        class_info.remove(class_info[3])
        class_info.append(link)
        class_info.append(link)
        print(class_info)

        cursor.execute("SELECT email FROM classes WHERE short_name = '{}'".format(new_class_short_name))
        teach_email = cursor.fetchall()[0][0]
        hf.send_email("Thank you for signing up to become a teacher at HELM Learning", email.format(*class_info), teach_email)

        try:
            reco_train.main()
        except:
            pass
        hf.stop(cnx, cursor)
    return jsonify(["0"])

@app.route('/api/v1/resources/signup_to_be_teach_2_5', methods=['GET'])
def signup_to_be_teach_2_5():
    cnx, cursor = hf.start()
    query_params = request.args
    short_name = query_params.get('name')
    cursor.execute("SELECT zoom FROM classes WHERE short_name = '{}'")
    try:
        isthereazoom = cursor.fetchall()[0][0]
        return jsonify(['1'])
    except:
        return jsonify(['0'])

@app.route('/api/v1/resources/signup_to_be_teach_3', methods=['GET'])
def signup_to_be_teach_3():
    cnx, cursor = hf.start()
    query_params = request.args
    short_name = query_params.get('name')
    short_name = short_name.replace('-', ' ')
    cursor.execute("SELECT zoom FROM classes WHERE short_name = '{}'")
    try:
        isthereazoom = cursor.fetchall()[0][0]
        return jsonify(['1'])
    except:
        print()
    # hf.send_email("Add the {} class to the website".format(short_name), "Sounds like a you problem CHIEF", 'vikramanantha@gmail.com', 'helmlearning2020@gmail.com')
    cursor.execute("SELECT teacher FROM classes WHERE short_name = '{}'".format(short_name))
    teacher = cursor.fetchall()[0][0]
    cursor.execute("SELECT short_name, email FROM classes WHERE short_name = '{}'".format(short_name))
    short_name_l = cursor.fetchall()[0]
    try:
        recording_link = hf.create_drive_folder("%s | (Sharing Materials)" % short_name_l[0], "18E91XtDTDVjNIOL9WPiAC1ozuKpNRR6e", colabs=short_name_l[1], anyone_permissions="reader")
    except:
        recording_link = "https://drive.google.com/drive/u/1/folders/18E91XtDTDVjNIOL9WPiAC1ozuKpNRR6e"
        # hf.send_email("BOEUFF ¶ Create Drive Folder", "Create shaaaring materials folder for the {} class".format(short_name_l[0]), "vikramanantha@gmail.com", "helmlearning2020@gmail.com")

    cursor.execute("UPDATE classes SET sharing_mats = '{}' WHERE short_name = '{}'".format(recording_link, short_name_l[0]))
    cnx.commit()
    hf.upload_simple_flyer(short_name_l[0])

    tes.et2_logistics(short_name, cursor)
    tes.et2_sharing(short_name, cursor)
    zoom_link = hf.createMeeting(short_name)
    cursor.execute("UPDATE classes SET zoom = '{}' WHERE short_name = '{}'".format(zoom_link, short_name))
    cursor.execute("UPDATE teachers SET display = '1' WHERE name = '{}'".format(teacher))
    cursor.execute("UPDATE classes SET display = '1' WHERE short_name = '{}'".format(short_name))
    hf.stop(cnx, cursor)
    return jsonify(["0"])

@app.route('/api/v1/resources/admin_schedule', methods=['GET'])
def schedule():
    cnx, cursor = hf.start()
    cursor.execute("SELECT short_name, starttime, endtime, day, startdate, enddate, zoom from classes WHERE startdate != '0000-00-00' ORDER BY startdate;")
    sqlclasses = cursor.fetchall()
    weeks = []
    classes = []
    # print(sqlclasses)
    for i in sqlclasses:
        # print("----------------------")
        short_name = i[0]
        time = datetime.strftime(hf.td_dt(i[1], "time"), "%-I:%M %p") + " - " + datetime.strftime(hf.td_dt(i[2], "time"), "%-I:%M %p")
        # print(time)
        # print()
        day = ""
        if i[3] == "weeklong":
            day = "Weeklong"
        else:
            day = i[3] + "s"
        date = day + ", " + datetime.strftime(hf.td_dt(i[4], "date"), "%b %d, %Y") + " - " + datetime.strftime(hf.td_dt(i[5], "date"), "%b %d, %Y")
        # print(date)
        # print()
        zoom = i[6]
        import timed_email_sending
        emails = timed_email_sending.ge(short_name, cursor)
        num_students = len(emails)
        if date not in weeks:
            weeks.append(date)
            classes.append([])
        classes[-1].append([short_name, time, date, zoom, num_students])
    # print(weeks)
    # print(classes)
    json = []
    for i in range(len(weeks)):
        listl = [weeks[i]]
        for j in range(len(classes[i])):
            listl.append({"Short_name": classes[i][j][0], "Time": classes[i][j][1], "Date": classes[i][j][2], "Zoom": classes[i][j][3], "Number_of_students": classes[i][j][4]})
        json.append(listl)
    # print(json)
    return jsonify(json)
    # return jsonify(
    #     [
    #         [
    #             "Weeklong: June 28 - July 2", 
    #             {'Short_name': 'Pineapples', 'Time': '18:00 - 19:00', 'Date': 'June 28 - July 02'},
    #             {'Short_name': 'Cantelope', 'Time': '15:00 - 16:00', 'Date': 'June 28 - July 02'},
    #         ],
    #         [
    #             "Weeklong: July 5 - July 9", 
    #             {'Short_name': 'Pineapples', 'Time': '18:00 - 19:00', 'Date': 'July 5 - July 9'},
    #             {'Short_name': 'Cantelope', 'Time': '15:00 - 16:00', 'Date': 'July 5 - July 9'},
    #         ]
    #     ]
    # )

@app.route('/api/v1/resources/admin_log', methods=['GET'])
def get_log():
    query_params = request.args
    filter = query_params.get('filter')
    lines = ""
    f = open("log.txt", "r")
    for x in f:
        if (filter in x or filter == "all"):
            lines = x + "<br><br>" + lines
    lines = lines.replace("]", "]")
    lines = lines.replace(" | ", "<br>---")
    buttons = ["Looking", "Signed up", "New Student", "Reco"]
    return jsonify([lines, buttons])

@app.route('/api/v1/resources/admin_students', methods=['GET'])
def admin_get_students():
    cnx, cursor = hf.start()
    limit = 100
    cursor.execute("Select Student_Name, Timestamp, Email_Address, City, State, Grade, Heard_about_us from students ORDER by Timestamp desc LIMIT %s;" % limit)
    students = cursor.fetchall()
    toreturn = ""
    for i in students:
        e = list(i)
        # e[0] = i[0].strftime("%b %d, %Y")
        ee = """
        {},<br>
        ----First Signup: {}<br>
        ----Email: {}<br>
        ----Lives in: {}, {}<br>
        ----Grade: {}<br>
        ----Heard about us: {}
        <br><br>
        """
        ee = ee.format(*e)
        toreturn += ee
    return jsonify([toreturn])

# Jul 3 2022
@app.route('/api/v1/resources/admin_stats', methods=['GET'])
def get_stats():
    cnx, cursor = hf.start()
    toreturn = []
    cursor.execute("select COUNT(*) from teachers")
    toreturn.append("Number of Teachers: %s" % cursor.fetchall()[0][0])
    intervals = [
        ['0000-00-00', '9999-12-31', 'All time'],
        "next",
    ]
    today = datetime.today()

    days = 7
    for i in range(0, days+1):
        begdaysago = today - timedelta(days=i)
        enddaysago = begdaysago + timedelta(days=1)
        intervals.append([begdaysago.strftime("%Y-%m-%d"), enddaysago.strftime("%Y-%m-%d"), "On %s" % begdaysago.strftime("%b %d")])
    intervals.append("next")

    weeks = 4
    for i in range(1, weeks+1):
        begdaysago = today - timedelta(days=i*7)
        enddaysago = begdaysago + timedelta(days=7)
        intervals.append([begdaysago.strftime("%Y-%m-%d"), enddaysago.strftime("%Y-%m-%d"), "%s - %s" % (begdaysago.strftime("%b %d"), enddaysago.strftime("%b %d"))])


    for i in intervals:
        if i == "next":
            toreturn.append("<br>")
            continue
        cursor.execute("select COUNT(*) from classes_to_students where timestamp >= '%s' and timestamp <= '%s'" % (i[0], i[1]))
        numsignups = cursor.fetchall()[0][0]
        cursor.execute("select COUNT(*) from students where timestamp >= '%s' and timestamp <= '%s'" % (i[0], i[1]))
        numstudents = cursor.fetchall()[0][0]
        toreturn.append("---- %s ----" % i[2])
        toreturn.append("%s signups" % (numsignups))
        toreturn.append("%s new Students" % (numstudents))
    

    return jsonify(toreturn)


@app.route('/api/v1/resources/login', methods=['GET'])
def login():
    cnx, cursor = hf.start()
    query_params = request.args
    email = query_params.get('email')
    pw = query_params.get('pw')
    sb = "SELECT pw, cipher FROM verify"
    cursor.execute(sb)
    pws = list(cursor.fetchall())
    the_real_ones = []
    for i in pws:
        i = list(i)
        the_real_ones.append(hf.decrypt(i[0], i[1]))
    if not (email == the_real_ones[1] and pw == the_real_ones[0]):
        return jsonify({'output': 0})
    access_token = hf.get_access_token()
    # print(access_token)
    
    return jsonify({
        'output': 1,
        'access_token': access_token
    })

@app.route('/api/v1/resources/check_login', methods=['GET'])
def check_login():
    cnx, cursor = hf.start()
    query_params = request.args
    access_token = query_params.get('token')
    status = hf.check_access_token(access_token); # returns a int, 1=good, 0=bad
    # print(status)
    return jsonify({'output':status})
    
@app.route('/api/v1/resources/sendesa', methods=['GET'])
def sendesa():
    cnx, cursor = hf.start()
    query_params = request.args
    short_name = query_params.get('short_name')
    short_name = short_name.replace("£", " ")
    classes_string = query_params.get('classes')
    classes_string = classes_string.replace("£", " ")
    if (', ' in classes_string):
        classes = classes_string.split(', ')
    elif ('; ' in classes_string):
        classes = classes_string.split('; ')
    elif (';' in classes_string):
        classes = classes_string.split(';')
    elif (',' in classes_string):
        classes = classes_string.split(',')
    else:
        classes = [classes_string]
    
    output, reason = tes.esa(short_name, cursor, classes)
    hf.stop(cnx, cursor)
    if output == 1:
        return jsonify({"output": 1, "failedclasses": reason})
    elif output == 2:
        return jsonify({"output": 2, "sentemails": reason[0], "totalemails": reason[1]})
    return jsonify({"output": 0})

# @app.route('/api/v1/resources/scarstoyourbeautiful', methods=['GET'])
# def showteacheremails():
#     cnx, cursor = hf.start()
#     cursor.execute("SELECT short_name, teacher, email FROM classes")
#     emails = cursor.fetchall()
#     return jsonify(emails)

@app.route('/api/v1/resources/everybodytrynastealmygirl', methods=['GET'])
def showteacheremails():
    cnx, cursor = hf.start()
    cursor.execute("SELECT short_name, starttime, endtime FROM classes")
    timedetails = cursor.fetchall()
    toreturn = []
    for i in timedetails:
        
        duration = i[2] - i[1]
        duration_in_s = duration.total_seconds() 
        minutes = divmod(duration_in_s, 60)[0]
        toreturn.append([i[0], minutes])
    return jsonify(toreturn)

@app.route('/api/v1/resources/get_teacher_info', methods=['GET'])
def get_teacher_info():
    try:
        cnx, cursor = hf.start()
        query_params = request.args
        classes = query_params.get('classes')
        classes = classes.replace('-', ' ')
        
        if (classes == "all"):
            toreturn = {}
            cursor.execute("SELECT name, yog, description, image, classes, ismanager FROM teachers WHERE display = '1'")
            asdf = cursor.fetchall()
            toreturn['Developers'] = []
            toreturn['Teachers'] = []
            toreturn['Managers'] = []
            toreturn['Speakers'] = []
            toreturn['Leaders'] = []
            toreturn['HELM Club Members'] = []

            roledict = ["HELM Club Member", "Leader", "Speaker", "Developer", "Manager", "Teacher"]

            for teachinfo in asdf:
                role = str(teachinfo[5]).zfill(6)
                # print(role)
                teacherroles = ""
                for i in range(len(role)):
                    if (int(role[i]) > 0):
                        teacherroles += roledict[i] + ", "
                teacherroles = teacherroles[:-2]

                teacher = {
                    "name": teachinfo[0],
                    "yog": teachinfo[1],
                    "description": teachinfo[2],
                    "image": teachinfo[3],
                    "classes": teachinfo[4].split(", "),
                    "role": teacherroles
                }
                # print(role)
                for i in range(len(role)):
                    # print(roledict[i] + "s")
                    if (role[i] == "1"): toreturn[roledict[i] + "s"].append(teacher)
                    # print(toreturn[roledict[i] + "s"])
                # toreturn["Teachers"].append({
                #     "name": teachinfo[0],
                #     "yog": teachinfo[1],
                #     "description": teachinfo[2],
                #     "image": teachinfo[3],
                #     "classes": teachinfo[4].split(", "),
                #     "role": "Teacher"
                # })
        else:
            toreturn = []
            class_id = hf.get_class_id(classes)
            cursor.execute("SELECT teacher_id FROM classes_to_teachers WHERE class_id = '{}'".format(class_id))
            teach_ids = cursor.fetchall()
            for i in teach_ids:
                cursor.execute("SELECT name, yog, description, image, email FROM teachers WHERE id = '{}'".format(i[0]))
                teachinfo = cursor.fetchall()[0]
                toreturn.append({
                    "name": teachinfo[0],
                    "yog": teachinfo[1],
                    "description": teachinfo[2],
                    "image": teachinfo[3],
                    "email": teachinfo[4],
                })
        # print(toreturn)
        return jsonify(toreturn)
        # return jsonify({
        #     "Teachers": [
        #         {
        #             "name": "Mr Picklez",
        #             "yog": "Class of 1847 at Bunker Hill Community College",
        #             "description": """Mr Picklez is a Feminism History teacher at the Squidward Community College. 
        #                             He is an avid music enjoyer, He enjoys playing the flute, saxaphone, piano, doorknob, violin, and clarinet. 
        #                             He also enjoys arguing with people on the internet that he has no say in.""",
        #             "image": "bit.ly/snakearms",
        #             "classes": ["c1"],
        #             "role": "Teacher, Leader"
        #         },
        #         {
        #             "name": "Mr Pototo",
        #             "yog": "Class of 2139 at MIT",
        #             "description": """Mr Pototo is a Feminism History teacher at the Squidward Community College. 
        #                             He is an avid music enjoyer, He enjoys playing the flute, saxaphone, piano, doorknob, violin, and clarinet. 
        #                             He also enjoys arguing with people on the internet that he has no say in.""",
        #             "image": "bit.ly/snakearms",
        #             "classes": ["c2"],
        #             "role": "Teacher"
        #         },
        #         {
        #             "name": "Mrs DeApple",
        #             "yog": "Class of 1492 at Sapulpa High School, OK",
        #             "description": """Mrs DeApple is a Feminism History teacher at the Squidward Community College. 
        #                             He is an avid music enjoyer, He enjoys playing the flute, saxaphone, piano, doorknob, violin, and clarinet. 
        #                             He also enjoys arguing with people on the internet that he has no say in.""",
        #             "image": "bit.ly/snakearms",
        #             "classes": ["c3"],
        #             "role": "Teacher"
        #         },
        #     ], 
        #     "Managers": [
        #         {
        #             "name": "Sir DelOrange",
        #             "yog": "Class of 1975 at Nashville High School",
        #             "description": """Sir DelOrange is a Feminism History teacher at the Squidward Community College. 
        #                             He is an avid music enjoyer, He enjoys playing the flute, saxaphone, piano, doorknob, violin, and clarinet. 
        #                             He also enjoys arguing with people on the internet that he has no say in.""",
        #             "image": "bit.ly/snakearms",
        #             "classes": ["c4"],
        #             "role": "Manager"
        #         },
        #         {
        #             "name": "Barrett The Carrot",
        #             "yog": "Class of 2021 at Arkansas State University",
        #             "description": """Barrett The Carrot is a Feminism History teacher at the Squidward Community College. 
        #                             He is an avid music enjoyer, He enjoys playing the flute, saxaphone, piano, doorknob, violin, and clarinet. 
        #                             He also enjoys arguing with people on the internet that he has no say in.""",
        #             "image": "bit.ly/snakearms",
        #             "classes": ["c7"],
        #             "role": "Manager"
        #         },
        #     ]
        #
        # })
    except:
        return jsonify([0])


@app.route('/api/v1/resources/get_classes_info', methods=['GET'])
def get_classes_info():
    cnx, cursor = hf.start()
    try:
        query_params = request.args
        filter = query_params.get('filter')
    except:
        filter = 'all'
    subjects = ['Science', 'Math', 'Coding', 'Humanities', 'Art', 'Other']
    classes = {}
    for i in subjects:
        classes[i] = []
    
    if (filter == 'archived'):
        sql = "SELECT name, short_name, teacher, icon, description, id FROM classes WHERE day = ''"
    elif (filter == 'current'):
        sql = "SELECT name, short_name, teacher, icon, description, id FROM classes WHERE day != ''"
    elif filter == 'async':
        sql = "SELECT name, short_name, teacher, icon, description, id FROM classes WHERE async_link != ''"
    else:
        sql = "SELECT name, short_name, teacher, icon, description, id FROM classes"
    cursor.execute(sql)

    des_classes = cursor.fetchall()
    for i in des_classes:
        # print(i)
        if (i[1][0].islower()):
            continue
        class_info = {
            "Name": i[0],
            "Signup Link": i[1].replace(" ", "-").lower(),
            "Teacher": i[2],
            "Icon": i[3],
            "Description": i[4]
        }
        class_id = i[-1]
        # display = i[-2]
        # if (display == 0): continue
        cursor.execute("SELECT tags.tag FROM tags INNER JOIN classes_to_tags ON tags.id = classes_to_tags.tag_id WHERE class_id = '{}';".format(class_id))
        tags = cursor.fetchall()
        accountedfor = False
        subjects_v2 = []
        for tag in tags:
            if (tag[0] in subjects):
                classes[tag[0]].append(class_info)
                accountedfor = True
        if (not accountedfor):
            classes["Other"].append(class_info)
        for i in subjects:
            temp = []
            for j in classes[i]:
                if j not in temp:
                    temp.append(j)
            # print(classes[i])
            classes[i] = temp
            if len(classes[i]) != 0:
                subjects_v2.append(i)
    # pprint({
    #     "Subjects": subjects,
    #     "Classes": classes
    # })
    return jsonify({
        "Subjects": subjects,
        "Classes": classes
    })


    # return jsonify({
    #     "Subjects": ["New", "Science"], 
    #     "Classes": {
    #     "New": [
    #         {"Name": "Class1", "Signup Link": "c1", "Teacher": "Mr Picklez", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class2", "Signup Link": "c2", "Teacher": "Mr Pototo", "Icon": "http://bit.ly/snakearms"}
    #     ],
    #     "Science": [
    #         {"Name": "Class3", "Signup Link": "c3", "Teacher": "Mrs DeApple", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class4", "Signup Link": "c4", "Teacher": "Sir DelOrange", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class5", "Signup Link": "c5", "Teacher": "Mr Banana", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class6", "Signup Link": "c6", "Teacher": "Prof La De L'Onion", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class7", "Signup Link": "c7", "Teacher": "Barrett The Carrot", "Icon": "http://bit.ly/snakearms"},
    #     ]
    # }})


@app.route('/api/v1/resources/upcomingclasses', methods=['GET'])
def upcomingclasses():
    cnx, cursor = hf.start()
    cursor.execute("SELECT name, short_name, teacher, startdate, icon FROM classes WHERE day = 'weeklong' and display = '1' ORDER BY startdate")
    classes = cursor.fetchall()
    weeklongs = []
    for i in classes:
        weeklongs.append({})
        weeklongs[-1]["Name"] = i[0]
        weeklongs[-1]["Signup Link"] = i[1].replace(" ", "-")
        weeklongs[-1]["Teacher"] = i[2]
        weeklongs[-1]["Dates"] = "Running the week of " + i[3].strftime("%b %d, %Y")
        weeklongs[-1]["Icon"] = i[4]

    cursor.execute("SELECT name, short_name, teacher, startdate, enddate, day, icon FROM classes WHERE day != '' AND day != 'weeklong' and display = '1' ORDER BY startdate")
    classes = cursor.fetchall()
    fiveweek = []
    for i in classes:
        fiveweek.append({})
        fiveweek[-1]["Name"] = i[0]
        fiveweek[-1]["Signup Link"] = i[1].replace(" ", "-")
        fiveweek[-1]["Teacher"] = i[2]
        fiveweek[-1]["Dates"] = "On " + i[5] + "s, " + i[3].strftime("%b %d") + " - " + i[4].strftime("%b %d")
        fiveweek[-1]["Icon"] = i[6]

    return jsonify({
        "Synchronous Weeklong Classes": weeklongs,
        "Synchronous 5 Week Classes": fiveweek,
    })
    # return jsonify({
    #     "Weeklong Classes":
    #     [
    #         {"Name": "Class1", "Signup Link": "c1", "Teacher": "Mr Picklez", "Dates": "Running the week of Aug 16, 2021", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class2", "Signup Link": "c2", "Teacher": "Mr Pototo", "Dates": "Running the week of Aug 16, 2021", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class3", "Signup Link": "c3", "Teacher": "Mrs DeApple", "Dates": "Running the week of Aug 23, 2021", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class4", "Signup Link": "c4", "Teacher": "Sir DelOrange", "Dates": "Running the week of Aug 23, 2021", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class5", "Signup Link": "c5", "Teacher": "Mr Banana", "Dates": "Running the week of Aug 30, 2021", "Icon": "http://bit.ly/snakearms"},
    #     ],
    #     "5 Week Classes":
    #     [
    #         {"Name": "Class6", "Signup Link": "c6", "Teacher": "Prof La De L'Onion", "Dates": "On Tuesdays, Sept 7 - Oct 4", "Icon": "http://bit.ly/snakearms"},
    #         {"Name": "Class7", "Signup Link": "c7", "Teacher": "Barrett The Carrot", "Dates": "On Wednesdays, Sept 8 - Oct 5", "Icon": "http://bit.ly/snakearms"},
    #     ]
    # })

@app.route('/api/v1/resources/get_num_students', methods=['GET'])
def get_num_students():
    cnx, cursor = hf.start()
    cursor.execute("SELECT COUNT(*) FROM classes_to_students")
    numstudents = cursor.fetchall()[0][0]
    numstudents = int(numstudents/100)
    numstudents = float(numstudents/10)

    cursor.execute("select COUNT(name) from teachers")
    numteachers = cursor.fetchall()[0][0]
    numteachers = int(float(int((numteachers * 2)/10)/2)*10)

    cursor.execute("select COUNT(name) from classes where startdate != '0000-00-00'")
    numsyncclasses = cursor.fetchall()[0][0]

    cursor.execute("select COUNT(name) from classes where async_link != ''")
    numasyncclasses = cursor.fetchall()[0][0]

    hf.stop(cnx, cursor)
    return jsonify({
        "Number of Students": "%sK" % numstudents, 
        "Number of Teachers": "%s" % numteachers,
        "Number of Synchronous Classes": "%s" % numsyncclasses,
        "Number of Asynchronous Classes": "%s" % numasyncclasses,
        "Number of Classes": str(numasyncclasses+numsyncclasses),
    })
    # return jsonify({"Number of Students": "%sK" % "3.8"})

@app.route('/api/v1/resources/contactusemail', methods=['GET'])
def contactus_email():
    cnx, cursor = hf.start()
    query_params = request.args
    name = query_params.get('name').replace("®", " ")
    email = query_params.get('email').replace("®", " ")
    message = query_params.get('message').replace("®", " ")

    subject = "Question aboot HELM"
    content = "We got a questionn:<br>Name: %s<br>Email: %s<br>-----------<br>%s" % (name, email, message)
    hf.send_email(subject, content, "helmlearning2020@gmail.com")
    return jsonify({"output": 1})

@app.route('/api/v1/resources/gettestimonialinfo', methods=['GET'])
def get_testimonial_info():
    news = [
        {
            "Title": "Lexington brothers offer free online classes, enroll students across America",
            "Author": "WickedLocal (Lexington MA)",
            "Link": "https://lexington.wickedlocal.com/news/20200430/lexington-brothers-offer-free-online-classes-enroll-students-across-america"
        },
        {
            "Title": "Community Service in the Era of COVID-19",
            "Author": "The Musket (Lexington High School, Lexington MA)",
            "Link": "https://lhsmusket.com/593/news/community-service-in-the-era-of-covid-19/"
        },
        {
            "Title": "In Conversation With HELM Learning Co-Founders",
            "Author": "Lokvani (Lexington MA)",
            "Link": "http://www.lokvani.com/lokvani/article.php?article_id=16998"
        },
        {
            "Title": "Jay Iyer is using his science smarts to share COVID-19 information and support medical research in his grandfather’s memory",
            "Author": "225BatonRouge (Baton Rouge LA)",
            "Link": "https://www.225batonrouge.com/our-city/hes-using-his-science-smarts-to-share-covid-19-information-and-support-medical-research-in-his-grandfathers-memory"
        },
        {
            "Title": "When students become teachers",
            "Author": "Metro West Daily News (Boston MA)",
            "Link": "https://www.metrowestdailynews.com/story/lifestyle/health-fitness/2020/05/09/when-students-become-teachers/1224667007/"
        },
    ]
    testimonials = [
        {
            "Message": "While Microbiology may seem like an advanced topic that only high schoolers and college students should be able to learn about, I had numerous elementary schoolers attend my class and they asked phenomenal questions!",
            "Person": "Jay Iyer, Instructor"
        },
        {
            "Message": "My son and daughter both signed up for the Chess class. They absolutely loved it! The instructor Ronak Wakhlu was amazing! He did an excellent job teaching the class. He made it easy for beginners to understand the concept of chess. He made the class fun and interactive! Highly recommend this class to any one who wants to learn or improve their chess skills!",
            "Person": "Rashmi Gupta, Parent",
        },
        {
            "Message": "My kids enjoyed the Chess class and every class built the interest and confidence in them. They were introduced to every piece one by one and learned how to use them using practice sessions. They became so confident that they challenged me couple of times, based on the confidence they got from playing in the Chess class.",
            "Person": "Monika Wadhwa, Parent",
        },
        {
            "Message": "My near-11 year old (going to 6th grade from coming Fall) loved it so much that he explained and ran his code (Python) to every family member who would listen (including myself and his grandparents!).",
            "Person": "Joyoni Dey, Parent",
        },
        {
            "Message": "A thoroughly enjoyable class! The instructor made valuable connections to modern microbiology research concerning the current coronavirus, was very concise, and was able to answer all questions in depth.",
            "Person": "Samantha Esselstyn, Student",
        },
    ]

    return jsonify({
        "News": news,
        "Testinomials": testimonials
    })

@app.route('/api/v1/resources/show_interest_teacher', methods=['GET'])
def show_interest_teacher():
    cnx, cursor = hf.start()
    query_params = request.args
    linfo = []
    lautre_classes = []
    length = query_params.get('length')
    position = query_params.get('position')
    hf.log("Potential teacher", "Interest Form", "")
    for i in range(int(length)):
        linfo.append(query_params.get(str(i)))
    lindexes = []
    for i in range(len(linfo)):
        linfo[i] = linfo[i].replace("º", " ")
    for i in linfo:
        i = i.replace('"', '`')
        i = i.replace("'", "„")
        cursor.execute('INSERT INTO cache (item) VALUES ("{}")'.format(i))
        cursor.execute('SELECT id FROM cache WHERE item = "{}"'.format(i))
        lindexes.append(cursor.fetchall()[-1][0])
    cache_locations = ""
    link = "http://teachers.helmlearning.com/signup?teacher&frominterest"
    for i in lindexes:
        link += "&" + hf.encode(i)
        cache_locations += "≈" + hf.encode(i)
    cache_locations = cache_locations[1:]
    hf.stop(cnx, cursor)
    return jsonify([
        0, cache_locations, link
    ])

@app.route('/api/v1/resources/send_interest_email', methods=['GET'])
def send_interest_email():
    cnx, cursor = hf.start()
    query_params = request.args
    cache_loca = query_params.get('cache')
    cache_locations = cache_loca.split("≈")
    decoded_cache_locations = []
    for i in cache_locations:
        decoded_cache_locations.append(hf.decode(i))
    stuffe = ["Name", "Email", "Town", "HeardAbout", "Short_Name"]
    for index, i in enumerate(decoded_cache_locations):
        cursor.execute("SELECT item from cache where id = '%s'" % i)
        stuffe[index] = cursor.fetchall()[0][0]

    link = "http://teachers.helmlearning.com/signup?teacher&frominterest&" + cache_loca.replace('≈', '&')

    content = """
    Hi {},<br>
    Thank you so much for your interest in teaching about {} at HELM Learning! If you would like to continue the teacher's form, <a href='{}'>click here</a>.<br>
    <br>
    See you soon!<br>
    Vikram from <strong style='color: #642c94'>HELM Learning</strong><br>
    """
    subject = "Teacher signup form link | HELM Learning"
    hf.send_email(subject, content.format(stuffe[0], stuffe[4], link), stuffe[1])
    content_2 = """
    Dude!! Someone is interested in the teacher thing!<br>
    {}<br>
    {}<br>
    """
    subject = "Dude! We got someone!!!!"
    hf.send_email(subject, content_2.format(stuffe[0], stuffe[4]), "vikramanantha@gmail.com")
    return jsonify([link])


@app.route('/api/v1/resources/save_signup_for_later', methods=['GET'])
def save_signup_for_later():
    try:
        cnx, cursor = hf.start()
        query_params = request.args
        linfo = []
        lautre_classes = []
        email = query_params.get('email')
        length = query_params.get('length')
        position = query_params.get('position')
        hf.log(email, "SaveForLater", "")
        for i in range(int(length)):
            linfo.append(query_params.get(str(i)))
        lindexes = []
        for i in range(len(linfo)):
            linfo[i] = linfo[i].replace("º", " ")
        for i in linfo:
            i = i.replace('"', '`')
            i = i.replace("'", "„")
            cursor.execute('INSERT INTO cache (item) VALUES ("{}")'.format(i))
            cursor.execute('SELECT id FROM cache WHERE item = "{}"'.format(i))
            lindexes.append(cursor.fetchall()[-1][0])
        # link = "http://teachers.helmlearning.com/signup?teacher&fromsfl"
        link = ""
        for i in lindexes:
            link += hf.encode(i) + "∑"
        link = link[:-1]
        hf.stop(cnx, cursor)
        return jsonify([
            0, link
        ])
    except Exception as e:
        print(e)
        return jsonify([1])


@app.route('/api/v1/resources/send_sfl_email', methods=['GET'])
def send_sfl_email():
    cnx, cursor = hf.start()
    query_params = request.args
    email = query_params.get('email')
    link = query_params.get('link')
    reallink = link.split("∑")
    
    # print(email)
    # print(link)
    # print(reallink)

    linkk = "http://teachers.helmlearning.com/signup?teacher&fromsfl&"
    for i in reallink:
        linkk += i + "&"
    linkk = linkk[:-1]
    # print(linkk)

    content = """
    Hi!<br>
    Here is the link which you can use to access the teacher signup page with all your responses:<br>
    <br>
    <a href='{}'>Save for later- Teacher sign up form link</a>.<br>
    <br>
    See you soon!<br>
    Vikram from <strong style='color: #642c94'>HELM Learning</strong><br>
    """
    subject = "Save for later- Teacher signup link [%s] | HELM Learning" % datetime.now().strftime("%b %-d, %Y")
    hf.send_email(subject, content.format(linkk), email)
    return jsonify([linkk, subject])


@app.route('/api/v1/resources/exchange_cache_2', methods=['GET'])
def exchange_cache_2():
    cnx, cursor = hf.start()
    query_params = request.args
    cache_loca = query_params.get('cache')
    cache_locations = cache_loca.split("≈")
    print(cache_loca, cache_locations)
    cache_locations = cache_locations[2:]
    decoded_cache_locations = []
    for i in cache_locations:
        decoded_cache_locations.append(hf.decode(i))
    print(decoded_cache_locations)
    stuffe = ["Name", "Email", "Town", "HeardAbout", "Short_Name"]
    for index, i in enumerate(decoded_cache_locations):
        cursor.execute("SELECT item from cache where id = '%s'" % i)
        dd = cursor.fetchall()[0][0]
        print(dd, index)
        stuffe[index] = dd
    hf.log(stuffe[0], "Signing up to teach", "")
    return jsonify(stuffe)

@app.route('/api/v1/resources/exchange_cache_3', methods=['GET'])
def exchange_cache_3():
    cnx, cursor = hf.start()
    query_params = request.url.split("?")[1]
    # print(query_params) ##¬¬¬
    sbali = query_params.split("&")
    toreturn = []
    for j in sbali:
        i = decode(j)
        try:
            notimportant = int(i)
        except:
            toreturn.append(i)
            continue
        try:
            cursor.execute("SELECT item FROM cache WHERE id = '{}'".format(i))
            dathing = cursor.fetchall()[0][0]
            dathing = dathing.replace("„", "'")
            dathing = dathing.replace("`", '"')
            toreturn.append(dathing)
        except:
            print("\n\nSomeone tampered with the system!! :O\n\n")
    return jsonify(toreturn)


@app.route('/api/v1/resources/unsubscribe', methods=['GET'])
def unsubscribe():
    cnx, cursor = hf.start()
    query_params = request.args
    fname = query_params.get("name")
    email = query_params.get("email")
    cursor.execute("select * from students where Student_Name = '%s' and (Email_Address = '%s' or Parent_Email = '%s')" % (fname, email,email))
    ids = cursor.fetchall()
    if (len(ids) == 0):
        return jsonify([1])
    cursor.execute("update students set Newsetter = '0' where Student_Name = '%s' and (Email_Address = '%s' or Parent_Email = '%s')" % (fname, email,email))
    hf.stop(cnx, cursor)
    return jsonify([0])

@app.route('/api/v1/resources/testerbester', methods=['GET'])
def testerbester():
    print("Tester Bester")
    return jsonify([0])


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    # return send_from_directory(app.static_folder, request.path[1:])
    return "User-agent: *\nDisallow: /"


    

'''
Steps to do:
    
PAGE 1:
    1. connect to correct database (line 34)
    2. update existing query (line 59) to search for name and email in table
    3. write new queries to search database to see if student has interests already
    4. write and send a JSON file with the determinator key in it
    

PAGE 2: receive JSON with user data and store in database
    1. read in a JSON file that has user data (lines 42-55), store in variables
    2. write and execute a query stores user data in a table (line 59)
    
    
PAGE 3: select interest fields from database and package into JSON, send to client. Receive JSON on interests, interpret and store in database
    1. search database for interests, select the interest (key name, key id) -- fetchall(), iterate through tuple and select data, reformat in a JSON file
    2. take interest data, write it into a JSON file, and export to webclient
    ---- user inputs data, JS collects user input and stores in JSON file ----
    3. read JSON file and store user interests in variables
    4. write query that inserts the user insterests into the database
    
PAGE 4: select class information from database and send it to webclient as JSON
    1. write a query that gets class info from the database and stores it as strings
    2. write a JSON file, and format that data inside the JSON file in JSON format
    3. push JSON file to webclient
    
    
'''
    


# app.run(host='0.0.0.0', debug=True, port=5000, ssl_context=('dumpsterfiles/cert3.pem', 'dumpsterfiles/key3.pem'))
app.run(host='0.0.0.0', port=5000, ssl_context=('/etc/letsencrypt/live/signup.helmlearning.com/fullchain.pem', '/etc/letsencrypt/live/signup.helmlearning.com/privkey.pem'))
# app.run(host='0.0.0.0', debug=True, port=5000)