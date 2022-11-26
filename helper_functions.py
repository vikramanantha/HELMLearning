#!/home/myuser/bin/python

# Vikram Anantha
# Dec 2 2020
# Helper functions used throughout all of the codes
# HELM Learning

from os import access
import sys; sys.path.append('/home/ec2-user/anaconda3/lib/python3.8/site-packages/mysql')
import smtplib as s
import ssl
import flask
import numpy
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np
import time
import string
import random
import datetime
from Google import Create_Service
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import requests
import json
from time import time
import http.client
import pyqrcode
import png
from PIL import Image, ImageDraw
from PIL import ImageTk, Image
from PIL import ImageGrab, ImageFont
from googleapiclient.http import MediaFileUpload
import boto
import boto.s3
from boto.s3.key import Key
import json
import logging
import boto3
from botocore.exceptions import ClientError
import io
from googleapiclient.http import MediaIoBaseDownload
from pprint import pprint
from datetime import datetime
import pytz
import requests
import json
import os
import base64
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders
import mimetypes

config = {
    'user': '[SECRET]',
    'password': '[SECRET]',
    'host': '[SECRET]', #52.21.172.100:22
    'port': '[SECRET]',
    'database': '[SECRET]'
}

days = {
    "Sunday": "1",
    "Monday": "2",
    "Tuesday": "3",
    "Wednesday": "4",
    "Thursday": "5",
    "Friday": "6",
    "Saturday": "7",
    "Tuesday,Thursday": "3,5",
    "Monday,Wednesday,Friday": "2,4,6",

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

def connect():
    db = "HELM_Database"
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    return cursor

def start():
    db = "HELM_Database"
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    # print("Connected!")
    return cnx, cursor

def stop(cnx, cursor):
    cnx.commit()
    cursor.close()
    cnx.close()
    # print("Disconnected!\n")
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

def get_time_v2(starttime, endtime):
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
    return time_est

def get_date_v2(day, startdate, enddate):
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
    # print(sdate)
    start_date = months[int(sdate[1])] + ' ' + sdate[2] + ', ' + sdate[0]
    end_date = months[int(edate[1])] + ' ' + edate[2] + ', ' + edate[0]
    phrase = ""
    if "weeklong" in day:
        phrase = "Mon-Fri, " + start_date + " - " + end_date
    else:
        phrase = day + "s, " + start_date + " - " + end_date
    return phrase

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
    # print(sdate)
    start_date = months[int(sdate[1])] + ' ' + sdate[2] + ', ' + sdate[0]
    end_date = months[int(edate[1])] + ' ' + edate[2] + ', ' + edate[0]
    return [start_date, end_date]

def encrypt(val, change):
    enc = ""
    count = 0
    for a in val:
        if count % 2 == 0:
            enc += chr((ord(a) + change) % 127)
        else:
            enc += chr((ord(a) - change) % 127)
    return enc

def decrypt(val, change):
    enc = ""
    count = 0
    for a in val:
        if count % 2 == 0:
            enc += chr((ord(a) - change) % 127)
        else:
            enc += chr((ord(a) + change) % 127)
    return enc

def get_id_from_student(fname, email=None):
    cnx, cursor = start()
    if email == None:
        sql = "SELECT id FROM students WHERE Student_Name = '{}'".format(fname)
    else:
        sql = "SELECT id FROM students WHERE Student_Name = '{}' AND Email_Address = '{}'".format(fname, email)
    cursor.execute(sql)
    sa = cursor.fetchall()
    try:
        student_id = sa[0][0]
    except:
        student_id = 2272
    return student_id

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
    print(x)
    return x

def get_related_classes(class_name):
    sorted_classes = []
    cnx, cursor = start()
    cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(class_name))
    class_id = cursor.fetchall()[0][0]
    cursor.execute("SELECT tag_id FROM classes_to_tags WHERE class_id = '{}'".format(class_id))
    tags = cursor.fetchall()
    tags = list(np.reshape(tags, (1, -1))[0])
    cursor.execute("SELECT id FROM classes")
    all_classes = cursor.fetchall()
    all_classes = list(np.reshape(all_classes, (1, -1))[0])
    for c in all_classes:
        if c == class_id:
            continue
        cursor.execute("SELECT tag_id FROM classes_to_tags WHERE class_id = '{}'".format(c))
        autre_tags = cursor.fetchall()
        autre_tags = list(np.reshape(autre_tags, (1, -1))[0])
        similarity = len(set(autre_tags) & set(tags))
        sorted_classes.append( [similarity, c] )

    sorted_classes.sort()
    sorted_classes = sorted_classes[::-1]
    to_return = []

    for i in sorted_classes:
        cursor.execute("SELECT short_name FROM classes WHERE id = '{}'".format(i[1]))
        cl = cursor.fetchall()[0][0]
        to_return.append(cl)
    
    return to_return
    stop(cnx, cursor)

def get_tags_from_classes(classes):
    cnx, cursor = start()
    sql0 = 'SELECT id FROM classes'
    cursor.execute(sql0)
    num_classes = cursor.fetchall()[-1][0]
    list_o_tags = []
    for i in classes:
        cursor.execute("SELECT tag_id FROM classes_to_tags WHERE class_id = '{}'".format(i))
        sb = cursor.fetchall()
        for j in sb:
            list_o_tags.append(j[0])
    list_o_tags = list(set(list_o_tags))
    to_return = []
    for i in range(3, num_classes+1):
        cursor.execute("SELECT tag_id FROM classes_to_tags WHERE class_id = '{}'".format(i))
        sb = np.array(cursor.fetchall())
        sb = list(np.reshape(sb, (1, -1))[0])
        # print(sb)
        numtags = len(set(sb) & set(list_o_tags))
        probs = 0
        if numtags >= 1:
            probs = 2
        if numtags >= 2:
            probs = 5
        if numtags >= 3:
            probs = 7
        if numtags >= 4:
            probs = 8
        to_return.append([i, probs])
    # print("\n\n")
    stop(cnx, cursor)
    return to_return

def create_drive_folder(folder_name, parent_folder_id, anyone_permissions=None, colabs=None):
    cnx, cursor = start()

    CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    folder = service.files().create(body=file_metadata).execute()
    folder_id = folder.get('id')

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        # else:
            # print("Permission Id: %s" % response.get('id'))
    user_permissions = "None"
    if anyone_permissions != None:
        batch = service.new_batch_http_request(callback=callback)
        for c in colabs.split(' and '):
            user_permissions = 'writer'
            user_permission = {
                'type': 'user',
                'role': user_permissions,
                'emailAddress': [c]
            }
            batch.add(service.permissions().create(
                    fileId=folder_id,
                    body=user_permission,
                    fields='id',
            ))
        domain_permission = {
            'type': 'anyone',
            'role': anyone_permissions, #'fileOrganizer', 'writer', 'commenter', 'reader'
        }
        batch.add(service.permissions().create(
                fileId=folder_id,
                body=domain_permission,
                fields='id',
        ))
        batch.execute()

    link = 'https://drive.google.com/drive/folders/%s?usp=sharing' % folder_id
    print("Folder successfully created!\n  %s\n  Shared with %s - %s,\n  Shared with AnyoneWithLink - %s" % (link, colabs, user_permissions, anyone_permissions))
    stop(cnx=cnx, cursor=cursor)
    return link

def send_email(subject, email, *recipients):
    # port = 465
    # sender = "helmlearning2020@gmail.com"
    # password = "[secret :)]"
    
    # message = MIMEMultipart("alternative")
    # message["Subject"] = subject
    # message["From"] = "HELM Learning"
    

    # # print(html)
    
    # part2 = MIMEText(email, "html")
    # message.attach(part2)
    # context = ssl.create_default_context()

    # print("\nSubject of this email: %s" % subject)
    # print(("To: " + "<{}>,\n    "*len(recipients)).format(*recipients))

    # for i in recipients:
    #     with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #         server.login(sender, password)
    #         message["To"] = i
    #         try:
    #             #input("send?")
    #             server.sendmail(sender, i, message.as_string())
    #             print("Sent!\n")
    #         except:
    #             print("NOT SENT\n")
    send_email_v2(subject, email, *recipients)

# send_email(
#     "Here comes the Sun",
#     "Test 2: Electric Boogaloo",
#     "vikramanantha@gmail.com",
#     "helmlearning2020@gmail.com"
# )


def send_email_v2(subject, email, *recipients):
    
    CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    for i in recipients:
        print("\n")
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = formataddr(('HELM Learning', 'helmlearning2020@gmail.com'))
            

            if (type(i) is tuple):
                message["To"] = formataddr((i[1], i[0]))
                message.attach(MIMEText(email.format(i[1]), "html"))
            else:
                message["To"] = i
                message.attach(MIMEText(email, "html"))

            print("Subject: %s" % message["Subject"])
            print("From: %s" % message["From"])
            print("To: %s" % message["To"])
        
            raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()
            message = service.users().messages().send(
                userId='me',
                body={'raw': raw_string}).execute()
            
            print(message['labelIds'][0])
        except:
            print("NOT SENT")
    print("\n")

# send_email_v2(
#     "Here comes the Sun",
#     "Hi {}, Test 2: Electric Boogaloo",
#     ("24anantha2@lexingtonma.org", "Vikram Anantha"),
#     ("dasmartone3141@gmail.com", "Mark Ananthanpillaichicfilla")
# )

# send_email_v2(
#     "Here comes the Sun",
#     "Hi, Test 2: Electric Boogaloo",
#     "24anantha2@lexingtonma.org",
#     "dasmartone3141@gmail.com",
# )

def get_legal_classes():
    cnx, cursor = start()
    classes_that_are_legal = []
    cursor.execute('SELECT id FROM classes')
    yessb = cursor.fetchall()
    for i in yessb:
        cursor.execute("SELECT COUNT(timestamp) FROM classes_to_students WHERE class_id = '{}' AND which = '1'".format(i[0]))
        yassss = cursor.fetchall()[0][0]
        if yassss != 0:
            classes_that_are_legal.append(i[0])
    stop(cnx, cursor)
    return classes_that_are_legal

def td_dt(delta, le_type):
    import datetime
    if le_type == "time":
        dt = datetime.datetime.strptime(str(delta), "%H:%M:%S")
    elif le_type == "date":
        dt = datetime.datetime.strptime(str(delta), "%Y-%m-%d")
    else:
        dt = datetime.datetime.strptime(str(delta), "%Y-%m-%d %H:%M:%S")
    return dt

def get_access_token():
    import datetime as dt
    cnx, cursor = start()
    length = random.randint(5, 10)
    token = ''
    for i in range(length):
        token += random.choice(string.ascii_letters)
    now = dt.datetime.now()
    farfromnow = now + dt.timedelta(hours=4)
    # print("CHECKING: ")
    # print(now)
    # print(farfromnow)
    cursor.execute("INSERT into access_tokens (token, opendate, closedate) VALUES ('%s', '%s', '%s')" % (token, now, farfromnow))
    stop(cnx, cursor)
    return token

def check_access_token(access_token):
    import datetime as dt
    cnx, cursor = start()
    now = dt.datetime.now()
    # print("CHECKING: ")
    # print(now)
    cursor.execute("SELECT token FROM access_tokens WHERE opendate <= '{}' AND closedate >= '{}'".format(now, now))
    tokens = cursor.fetchall()
    stop(cnx, cursor)
    for i in tokens:
        print("[%s] == [%s] : %s" % (i[0], access_token, i[0]==access_token))
        if i[0] == access_token:
            return 1
    
    return 0

def generateToken():
    API_KEY = 'rZMt2mQlTNuNFDU6ALLAcA'
    API_SEC = 'Df6QqyUtG3xOs1eW7ABah11GdyC7HqXCUW3J'
    token = jwt.encode(
        # Create a payload of the token containing API Key & expiration time
        {"iss": API_KEY, "exp": time() + 5000},
        # Secret used to generate token signature
        API_SEC,
        # Specify the hashing alg
        algorithm='HS256'
        # Convert token to utf-8
    )

    return token

def createMeeting(short_name):
    cnx, cursor = start()
    cursor.execute("SELECT starttime FROM classes WHERE short_name='{}'".format(short_name))
    starttime = cursor.fetchall()[0][0]
    cursor.execute("SELECT startdate FROM classes WHERE short_name='{}'".format(short_name))
    startdate = cursor.fetchall()[0][0]
    cursor.execute("SELECT day FROM classes WHERE short_name='{}'".format(short_name))
    day = cursor.fetchall()[0][0]
    if (day == 'weeklong'): 
        reccurence = {
            "type": 1,
            "repeat_interval": 1,
            "end_times": 7
        }

    else: 
        reccurence = {
            "type": 2,
            "repeat_interval": 1,
            "weekly_days": days[day],
            "end_times": 7
        }


    meetingdetails = {"topic": "%s" % short_name,
				"type": 8,
				"start_time": "%sT%s" % (startdate, starttime),
				"duration": "60",
				"timezone": "America/New York",
				"agenda": "HELM",
                "password": "PreMalone",
				"recurrence": reccurence,
				"settings": {"host_video": "true",
							"participant_video": "false",
							"join_before_host": "False",
							"mute_upon_entry": "true",
							"audio": "voip",                            
							}
				}
    
    headers = {'authorization': 'Bearer %s' % generateToken(),
			'content-type': 'application/json'}
    r = requests.post(
		f'https://api.zoom.us/v2/users/me/meetings',
	headers=headers, data=json.dumps(meetingdetails))
    
    print("\n creating zoom meeting ... \n")
	# print(r.text)
	# converting the output into json and extracting the details
    y = json.loads(r.text)
	# print(
	# 	y
    # )
    join_URL = y["join_url"]
    starttime = y["occurrences"][0]['start_time']
    meetingPassword = y["password"]
    
    # print(
	# 	'Zoom Meeting Link: {} \nPw: "{}"\n'.format(join_URL, meetingPassword)
    # )
    print("Created a zoom meeting %s \nStarting on %s" % (join_URL, starttime))
    # pprint(y)
    # pprint(meetingdetails)
    stop(cnx, cursor)
    return join_URL

def generate_qrcode(classname):
    output = 'dumpsterfiles/%s_qrcode.png' % classname.lower().replace(" ", "-")
    qr = pyqrcode.create("http://signup.helmlearning.com/page1.html?class=%s" % classname.lower().replace(" ", "-"))
    qr.png(output, scale=6, quiet_zone=1)
    print("Created QR Code for the %s class (put into folder %s" % (classname, output))

def generate_simple_flyer(classname):

    fontfam = "dumpsterfiles/productsans.ttf"
    fontfambold = "dumpsterfiles/productsans-bold.ttf"
    output = "dumpsterfiles/%s_simple_flyer.png" % classname.lower().replace(" ", "-")

    im = Image.new('RGBA', (800, 800), (99, 44, 148, 255))
    draw = ImageDraw.Draw(im) 

    w, h = draw.textsize("Want to Learn\n%s\nfor FREE?" % classname, font=ImageFont.truetype(fontfambold, 110))
    if (w > 800):
        fontsize = 85
        w, h = draw.textsize("Want to Learn\n%s\nfor FREE?" % classname, font=ImageFont.truetype(fontfambold, 85))
    else:
        fontsize = 110
    draw.text(((800-w)/2, 50), "Want to Learn\n%s\nfor FREE?" % classname, align="center", fill="white", font=ImageFont.truetype(fontfambold, fontsize))
    w, h = draw.textsize("Find more\ndetails for the\n%s\nclass at HELM\nto learn for\nFREE!" % classname, font=ImageFont.truetype(fontfam, 33))
    draw.text((545-w, 580), "Find more\ndetails for the\n%s\nclass at HELM\nto learn for\nFREE!" % classname, fill="white", font=ImageFont.truetype(fontfam, 33), align='right')

    generate_qrcode(classname)

    im2 = Image.open('dumpsterfiles/%s_qrcode.png' % classname.lower().replace(" ", "-"))
    im2 = im2.resize((250, 250), Image.BOX)
    im.paste(im2, (550, 550))

    draw.text((550, 495), "signup.helmlearning.com\n?%s" % classname.lower().replace(" ", "-"), fill="white", font=ImageFont.truetype(fontfam, 22), align="center")

    im2 = Image.open('logo.png')
    im2 = im2.resize((270, 90), Image.BOX)
    im.paste(im2, (0, 710), im2)

    im.save(output)
    print("Simple Flyer Created for the %s class (in the folder %s)" % (classname, output))
    return output

def generate_flyer_v2(classname):
    fontfam = "dumpsterfiles/productsans.ttf"
    fontfambold = "dumpsterfiles/productsans-bold.ttf"
    output = "dumpsterfiles/%s_flyer_v2.png" % classname.lower().replace(" ", "-")
    im = Image.new('RGBA', (600, 600), (102, 45, 145, 250))
    draw = ImageDraw.Draw(im) 

    w, h = draw.textsize("Learn\n%s\nfor FREE!" % classname, font=ImageFont.truetype(fontfambold, 80))
    draw.text(((600-w)/2, 0), "Learn\n%s\nfor FREE!" % classname, align="center", fill="white", font=ImageFont.truetype(fontfambold, 80))

    w, h = draw.textsize("Learn %s for FREE from content\ncreated by HELM student-teachers\nfrom MIT, Harvard, LHS, and more!" % classname, font=ImageFont.truetype(fontfambold, 30))
    # print(w)
    draw.text((300-(w/2), 280), "Learn %s for FREE from content\ncreated by HELM student-teachers\nfrom MIT, Harvard, LHS, and more!" % classname, fill="white", font=ImageFont.truetype(fontfambold, 30), align='center')

    # if (not os.path.exists('dumpsterfiles/%s_qrcode.png')):
    generate_qrcode(classname)

    im2 = Image.open('dumpsterfiles/%s_qrcode.png' % classname.lower().replace(" ", "-"))
    im2 = im2.resize((200, 200), Image.BOX)
    im.paste(im2, (400, 400))

    w,h = draw.textsize("signup.helmlearning.com?%s" % classname.lower().replace(" ", "-"), font=ImageFont.truetype(fontfambold, 20))
    draw.text(((400-w)/2, 420), "Scan the QR code or go to", fill="white", font=ImageFont.truetype(fontfam, 20), align="left")
    draw.text(((400-w)/2, 440), "signup.helmlearning.com?%s" % classname.lower().replace(" ", "-"), fill="white", font=ImageFont.truetype(fontfambold, 20), align="left")

    im2 = Image.open('logo.png')
    im2 = im2.resize((210, 70), Image.BOX)
    im.paste(im2, (0, 530), im2)

    # im.show()
    im.save(output)
    print("Flyer V2 Created for the %s class (in the folder %s)" % (classname, output))
    return output


def upload_file_to_folder(filename, filepath, parent_folder_id):
    CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


    # Upload a file
    file_metadata = {
        'name': filename,
        'parents': [parent_folder_id]
    }

    media_content = MediaFileUpload(filepath, mimetype='image/png')

    file = service.files().create(
        body=file_metadata,

        media_body=media_content
    ).execute()

    print("%s has been uploaded to Google Drive Folder with ID %s" % (filename, parent_folder_id))

def download_googledrive_image(link, file_name):
    CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    try:
        id = link.split("/")[-2]
    except:
        return 1
    request = service.files().get_media(fileId=id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('Download progress {0}'.format(status.progress() * 100))
    # print("\n1.\n")
    fh.seek(0)
    # print("\n2.\n")
    with open(file_name, 'wb') as f:
        f.write(fh.read())
        f.close()
    # print("\n3.\n")
    # print(file_name)
    # im = Image.open(file_name)
    # print("\n4.\n")
    # width, height = im.size
    # print("\n5.\n")
    # if (width < height):
    #     print("\n6.\n")
    #     left = 0 
    #     top = 200
    #     right = width
    #     bottom = top+width
    #     print("\n7.\n")
    # elif (height < width):
    #     print("\n8.\n")
    #     left = (width/2) - (height/2)
    #     top = 0
    #     right = (width/2) + (height/2)
    #     bottom = height
    #     print("\n9.\n")

    # print("\n10.\n")
    # im1 = im.crop((left, top, right, bottom))
    # im1.save(file_name)
    # print("\n11.\n")
    return 0

def upload_simple_flyer(classname):
    generate_simple_flyer(classname)

    cnx, cursor = start()
    cursor.execute("SELECT sharing_mats FROM classes WHERE short_name = '{}'".format(classname))
    sharingmats_drivefolder = cursor.fetchall()[0][0]
    parent_folder_id = sharingmats_drivefolder[39:-12]

    filename = "%s Simple Flyer" % classname
    filepath = "dumpsterfiles/%s_simple_flyer.png" % classname.lower().replace(" ", "-")

    upload_file_to_folder(filename, filepath, parent_folder_id)
    print("\nSimple Flyer has Sucessfully been uploaded to the Sharing Materials Folder")

def upload_file_to_s3(bucket, file_name, object_name=None):
    aws_secret_stuff = json.load(open('aws-secret.json'))
    AWS_ACCESS_KEY_ID = aws_secret_stuff['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = aws_secret_stuff['AWS_SECRET_ACCESS_KEY']
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    
    # Upload the file
    s3_client = boto3.client('s3',
         aws_access_key_id=AWS_ACCESS_KEY_ID,
         aws_secret_access_key= AWS_SECRET_ACCESS_KEY)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
        print('Uploaded %s to Amazon S3 bucket %s' % (file_name, bucket))
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
def get_class_id(classname):
    cnx, cursor = start()
    print("SELECT id FROM classes WHERE short_name='{}'".format(classname))
    cursor.execute("SELECT id FROM classes WHERE short_name='{}'".format(classname))
    try:
        class_id = cursor.fetchall()[0][0]
        return int(class_id)
    except:
        return -1

def is_teacher_is_in_db(cursor, teachername, teacheremail):
    cursor.execute("SELECT COUNT(id) FROM teachers WHERE name = '{}' AND email = '{}'".format(teachername, teacheremail))
    numteach = cursor.fetchall()[0][0]
    return numteach != 0

def add_teacher_to_db(info, format=['name', 'email', 'phonenumber', 'yog', 'description', 'image', 'classes', 'ismanager', 'display']):
    cnx, cursor = start()
    print("ADDING TEACHER TO THE DB")
    isteach = is_teacher_is_in_db(cursor, info[format.index("name")], info[format.index("email")])
    if (not isteach):
        print(format)
        print(info)
        cursor.execute("INSERT INTO teachers ({}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\");".format(*format, *info))
        print("%s has been added to the database!" % info[format.index("name")])
        cnx.commit()
    else:
        cursor.execute("SELECT classes FROM teachers WHERE name = '{}' AND email = '{}'".format(info[format.index("name")], info[format.index("email")]))
        cls = cursor.fetchall()[0][0];
        if (cls == info[format.index("classes")]):
            return
        cursor.execute("UPDATE teachers SET classes = '{}' WHERE name = '{}' AND email = '{}'".format(
            cls + ", " + info[format.index("classes")],
            info[format.index("name")], info[format.index("email")],
        ))
        print("Updated %s's classes from \n%s to \n%s" % (info[format.index("name")], cls, cls + ", " + info[format.index("classes")]))
    cursor.execute("SELECT id FROM teachers WHERE name = '{}' AND email = '{}'".format(info[format.index("name")], info[format.index("email")]))
    teacher_id = cursor.fetchall()[0][0]
    print("Added these classes to the teacher:")
    try:
        for i in info[format.index("classes")].split(", "):
            cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(i))
            class_id = cursor.fetchall()[0][0]
            
            cursor.execute("SELECT id FROM teachers WHERE name = '{}' AND email = '{}'".format(info[format.index("name")], info[format.index("email")]))
            teacher_id = cursor.fetchall()[0][0]
            cursor.execute("INSERT INTO classes_to_teachers (class_id, teacher_id) VALUES ('{}', '{}')".format(class_id, teacher_id))
            print("  %s >> %s" % (teacher_id, class_id))
    except:
        pass
    stop(cnx, cursor)
    return teacher_id

# def log(message):
#     f = open("log.txt", "a")
#     now = datetime.now(pytz.timezone('America/New_York') )
#     timestamp = now.strftime("%H:%M:%S (EST) - %b %d %Y")
#     f.write("[%s] %s\n" % (timestamp, message))
#     f.close()

def log(who, what, where, when=None):
    f = open("log.txt", "a")
    if when == None:
        now = datetime.now(pytz.timezone('America/New_York') )
        when = now.strftime("%H:%M:%S (EST) - %b %d %Y")

    place = location_from_ip_address()
    
    f.write("[%s] | %s | %s | %s | %s\n" % (when, space(what), space(who), space(place), where))
    f.close()

def location_from_ip_address():
    ip_address = flask.request.remote_addr
    try:
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result = json.loads(result)
        place = "%s %s" % (result['country_code'], result['city'])
    except:
        place = str(ip_address)
    return place

def space(word, num=15):
    news = str(word)
    toadd = num - len(news)
    if toadd < 0:
        news = news[:num-1] + '…'
    else:
        news += " "*toadd
    return news