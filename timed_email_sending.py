#!/home/myuser/bin/python

# Vikram Anantha
# Sept 3 2020
# Sending every mass email to teachers and students
# HELM Learning

not_sent_emails = []
import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import sys; sys.path.append('/home/ec2-user/anaconda3/lib/python3.8/site-packages/mysql')
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import helper_functions
from create_class_recordings_folder import *

did_the_emails_fail_to_send = [False, 0, 0]

def send(name_of_email, subject, content, student_fname, email, pemail, list_of_content, extra_content = None):
    send_v2(name_of_email, subject, content, student_fname, email, pemail, list_of_content, extra_content)
    # port = 465
    # sender = "helmlearning2020@gmail.com"
    # password = "[secret]"
    
    # message = MIMEMultipart("alternative")
    # message["Subject"] = subject.format(list_of_content[0])
    # message["From"] = "HELM Learning"
    # message["To"] = email
    # if (' and ' in email):
    #     spit_emails = email.split(' and ')
    #     email = spit_emails[0]
    #     pemail = spit_emails[1]

    # if name_of_email == "e1" or name_of_email == "er1":
    #     if extra_content == "weeklong":
    #         content = content.replace("5 Weeks, once per week)", "5 days in a week, Mon-Fri)")
    #     elif extra_content != None: 
    #         content = content.replace("5 Weeks, once per week)", extra_content)  
    #     elif ", " in list_of_content[5]:
    #         content = content.replace("5 Weeks, once per week)", "A couple weeks long on %s)" % list_of_content[5])  
    
    # elif name_of_email == "esa":
    #     breaf = list_of_content[0]
    #     list_of_content[0] = list_of_content[1]
    #     list_of_content[1] = breaf
    
    # if name_of_email == "e4":
    #     encoded_student_id = helper_functions.encode(helper_functions.get_id_from_student(fname=student_fname, email=email))
    #     print(("{}\n"*len(list_of_content)).format(*list_of_content))
    #     print("\n\n-------and now-------\n\n")
    #     list_of_content.insert(1, encoded_student_id)
    #     list_of_content.insert(3, encoded_student_id)
    #     print(("{}\n"*len(list_of_content)).format(*list_of_content))

    #     print(content.format(
    #         student_fname[0].upper() + student_fname[1:], 
    #         *list_of_content))
    # html = content.format(
    #     student_fname[0].upper() + student_fname[1:], 
    #     *list_of_content
    # )

    # if name_of_email == "esa":
    #     breaf = list_of_content[0]
    #     list_of_content[0] = list_of_content[1]
    #     list_of_content[1] = breaf
    # # print(html)
    
    # part2 = MIMEText(html, "html")
    # message.attach(part2)
    # context = ssl.create_default_context()
    

    # with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #     try:
    #         server.login(sender, password)
    #     except:
    #         did_the_emails_fail_to_send[0] = True
    #     try:
    #         #input("send?")
    #         server.sendmail(sender, email, message.as_string())
    #         print("Sent!\n")
    #     except:
    #         print("NOT SENT\n")
    #         not_sent_emails.append(email)
    # if pemail != None:
    #     with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #         server.login(sender, password)
    #         try:
    #             #input("send?")
    #             server.sendmail(sender, pemail, message.as_string())
    #             print("Sent!\n")
    #         except:
    #             print("NOT SENT\n")
    #             not_sent_emails.append(pemail)

    # # FLABBERGAS
    # if name_of_email == "e4":
    #     list_of_content.remove(encoded_student_id)
    #     list_of_content.remove(encoded_student_id)

les_emails_de_lemail = set()

def send_v2(name_of_email, subject, content, student_fname, email, pemail, list_of_content, extra_content = None):
    global les_emails_de_lemail
    if (' and ' in email):
        spit_emails = email.split(' and ')
        email = spit_emails[0]
        pemail = spit_emails[1]
    
    if name_of_email == "e1" or name_of_email == "er1":
        if extra_content == "weeklong":
            content = content.replace("5 Weeks, once per week)", "5 days in a week, Mon-Fri)")
        elif extra_content != None: 
            content = content.replace("5 Weeks, once per week)", extra_content)  
        elif ", " in list_of_content[5]:
            content = content.replace("5 Weeks, once per week)", "A couple weeks long on %s)" % list_of_content[5]) 
    elif name_of_email == "esa":
        breaf = list_of_content[0]
        list_of_content[0] = list_of_content[1]
        list_of_content[1] = breaf
    elif name_of_email == "e4":
        encoded_student_id = helper_functions.encode(helper_functions.get_id_from_student(fname=student_fname, email=email))
        list_of_content.insert(1, encoded_student_id)
        list_of_content.insert(3, encoded_student_id)

    html = content.format(
        "{}", 
        *list_of_content
    )

    if name_of_email == "esa":
        breaf = list_of_content[0]
        list_of_content[0] = list_of_content[1]
        list_of_content[1] = breaf

    if (email in les_emails_de_lemail or pemail in les_emails_de_lemail):
        return
    
    les_emails_de_lemail.add(email)
    les_emails_de_lemail.add(pemail)
    
    helper_functions.send_email_v2(
        subject.format(list_of_content[0]),
        html,
        (email, student_fname[0].upper() + student_fname[1:]),
        (pemail, student_fname[0].upper() + student_fname[1:])
    )

    if name_of_email == "e4":
        list_of_content.remove(encoded_student_id)
        list_of_content.remove(encoded_student_id)



config = {
    'user': 'helmlearning',
    'password': ':RYP9Y,37:mDm',
    'host': 'helmlearningdatabase-1.cnoqlueuri3g.us-east-1.rds.amazonaws.com', #52.21.172.100:22
    'port': '3306',
    'database': 'HELM_Database'
}
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

cnx, cursor = helper_functions.start()
cursor.execute("SELECT * FROM important_dates WHERE kind='1'")
skipping_weeks = cursor.fetchall()
helper_functions.stop(cnx=cnx, cursor=cursor)

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
    

def e1(class_name, cursor):
    sql5 = 'SELECT id, last_student FROM classes WHERE short_name = "{}"'.format(class_name)
    sql4 = 'SELECT student_id FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}"'
    sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, day, startdate, day, enddate, zoom, zoom, e1_additionalwork, teacher, email, name FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
    sql3 = 'SELECT subject, content FROM templates WHERE name="{}"'.format("e1")
    sql = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = {}'
    sql_e2 = 'SELECT student_cap FROM classes WHERE short_name = "{}"'.format(class_name)
    cursor.execute(sql_e2)
    student_cap = cursor.fetchall()[0][0]
    if student_cap != -1:
        e2(class_name, cursor)
        return
    cursor.execute(sql5)
    class_asdf = cursor.fetchall()[0]
    class_id = class_asdf[0]
    last_stud = class_asdf[1]

    if (last_stud == None):
        last_stud = "0000-00-00 00:00:00"
    cursor.execute(sql4.format(class_id, last_stud))
    student_ids = cursor.fetchall()

    cursor.execute(sql2)
    class_info = list(cursor.fetchall()[0])

    cursor.execute(sql3)
    stuff = cursor.fetchall()[0]
    email_info = []
    email_info.append(stuff[0])
    email_info.append(stuff[1])
    time_est = helper_functions.gettime(class_info[3], class_info[4])[0]
    time_cst = helper_functions.gettime(class_info[3], class_info[4])[1]
    class_info[3] = time_est
    class_info[4] = time_cst
    startdate = helper_functions.getdate(class_info[6], class_info[8])[0]
    enddate = helper_functions.getdate(class_info[6], class_info[8])[1]

    import datetime
    skipclass = None
    for i in skipping_weeks:
        if class_info[6] < datetime.date(i[0], i[1], i[2]) and class_info[8] > datetime.date(i[0], i[1], i[2]):
            skipclass = "5 Weeks, once per week)<br><strong>{}</strong>".format(i[3])

    class_info[6] = startdate
    class_info[8] = enddate

    if "weeklong" in class_info[5]:
        skipclass = "weeklong"
        class_info[5] = "Monday"
        class_info[7] = "Friday"

    # print(class_info)
    emails = []
    for j in student_ids:
        i = j[0]
        # print(i)
        cursor.execute(sql.format(i))
        try:
            theemails = cursor.fetchall()[0]
        except:
            continue
        if (list(theemails) not in emails):
            emails.append(list(theemails))
    # sql_teacher_email = "SELECT email,email,teacher FROM classes WHERE id = '{}'".format(class_id)
    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0] + ",<br>The following email is an automated email about Welcome details for your class sent out to all of the students in this session of your class. (Note: You do not need to do anything with this email)<br><br>---------------------------------------------<br><br>Hello Totally Real Student"
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)
    
    prep_to_send("e1", emails, email_info, class_info, qwert=[skipclass])

def e2(class_name, cursor):
    emails = []
    waitlist_emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "%s"' % class_name
    sql2 = 'SELECT last_student, final_student FROM classes WHERE short_name = "%s"' % class_name
    sql3 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql35 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}"'
    sql4 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql5 = 'SELECT name, teacher, e1_summary, starttime, endtime, day, startdate, day, enddate, zoom, zoom, e1_additionalwork, teacher, email, name FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
    sql55 = 'SELECT name, teacher, name FROM classes WHERE short_name = "%s";' % class_name
    sql6 = 'SELECT subject, content FROM templates WHERE name="e1"'
    sql65 = 'SELECT subject, content FROM templates WHERE name="e2"'
    # print("1")
    cursor.execute(sql)
    class_id = cursor.fetchall()[0][0]
    # print("2")
    cursor.execute(sql2)
    fila_student = cursor.fetchall()[0]
    # print(fila_student[0])
    cursor.execute(sql3.format(class_id, fila_student[0], fila_student[1]))
    welcome_studentids = cursor.fetchall()
    # print("4")
    cursor.execute(sql35.format(class_id, fila_student[1]))
    waitlist_studentids = cursor.fetchall()
    for i in welcome_studentids:
        cursor.execute(sql4.format(i[0]))
        try:
            student_info = cursor.fetchall()[0]
        except:
            continue
        if (student_info not in emails):
            emails.append(student_info)
    for i in waitlist_studentids:
        cursor.execute(sql4.format(i[0]))
        try:
            student_info = cursor.fetchall()[0]
        except:
            continue
        if (student_info not in waitlist_emails):
            waitlist_emails.append(student_info)
    # print("5")
    cursor.execute(sql5)
    welcome_classinfo = list(cursor.fetchall()[0])
    # timeest = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[0]
    # timecst = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[1]
    # startdate = helper_functions.getdate(welcome_classinfo[5], welcome_classinfo[6])[0]
    # enddate = helper_functions.getdate(welcome_classinfo[5], welcome_classinfo[6])[1]
    # welcome_classinfo[3] = timeest
    # welcome_classinfo[4] = timecst
    # welcome_classinfo[5] = startdate
    # welcome_classinfo[6] = enddate
    # print(welcome_classinfo)
    time_est = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[0]
    time_cst = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[1]
    welcome_classinfo[3] = time_est
    welcome_classinfo[4] = time_cst
    startdate = helper_functions.getdate(welcome_classinfo[6], welcome_classinfo[8])[0]
    enddate = helper_functions.getdate(welcome_classinfo[6], welcome_classinfo[8])[1]

    import datetime
    skipclass = None
    for i in skipping_weeks:
        if welcome_classinfo[6] < datetime.date(i[0], i[1], i[2]) and welcome_classinfo[8] > datetime.date(i[0], i[1], i[2]):
            skipclass = "5 Weeks, once per week)<br><strong>{}</strong>".format(i[3])

    welcome_classinfo[6] = startdate
    welcome_classinfo[8] = enddate

    if "weeklong" in welcome_classinfo[5]:
        welcome_classinfo[5] = "Monday"
        welcome_classinfo[7] = "Friday"

    for i in range(len(welcome_classinfo)):
        if welcome_classinfo[i] == None:
            welcome_classinfo[i] = ''
    # print("6")
    cursor.execute(sql55)
    waitlist_classinfo = cursor.fetchall()[0]
    # print(waitlist_classinfo)
    # print("7")
    cursor.execute(sql65)
    waitlist_emailinfo = cursor.fetchall()[0]
    # print("7.5")
    cursor.execute(sql6)
    email_info = cursor.fetchall()[0]
    # print("8")
    for i in range(0, len(welcome_classinfo)):
        if (welcome_classinfo[i] == None):
            welcome_classinfo[i] == ''
    for i in range(0, len(waitlist_classinfo)):
        if (waitlist_classinfo[i] == None):
            waitlist_classinfo[i] == ''

    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0] + ",<br>The following email is an automated email about Welcome details for your class sent out to all of the students in this session of your class. (Note: You do not need to do anything with this email)<br><br>---------------------------------------------<br><br>Hello Totally Real Student"
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)
    prep_to_send("e2", emails, email_info, welcome_classinfo=welcome_classinfo, waitlist_emails=waitlist_emails, waitlist_emailinfo=waitlist_emailinfo, waitlist_classinfo=waitlist_classinfo)

def esa(class_name, cursor, classes):
    emails = []
    #subject_area = input("Subject Area? ")

    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id FROM classes_to_students WHERE class_id = "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT short_name, name, short_name, description, teacher, starttime, endtime, startdate, enddate, day FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="esa"'


    qwert = {}
    print("These are the classes that will be sent out the email:\n%s" % classes)
    failedclasses = []
    for k in classes:
        try:
            cursor.execute(sql.format(k))
            class_id = cursor.fetchall()[0][0]
        except:
            failedclasses.append(k)
            continue
        cursor.execute(sql2.format(class_id))
        students = cursor.fetchall()
        for qw in students:
            cursor.execute(sql3.format(qw[0]))
            try:
                emaillist = list(cursor.fetchall()[0])
            except:
                continue
            emaillist.append(k)
            if (list(emaillist) not in emails):
                emails.append(list(emaillist))
                qwert[emaillist[0]] = k
    if len(failedclasses) > 0:
        return 1, failedclasses
    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])

    #class_info.insert(0, input("subject_area"))
    class_info[5] = helper_functions.gettime(class_info[5], class_info[6])[0]
    class_info.remove(class_info[6])
    if (helper_functions.getdate(class_info[6], class_info[7])[0] != "TBD"):
        if ("weeklong" in class_info[8]):
            class_info[6] = "Monday - Friday, " + helper_functions.getdate(class_info[6], class_info[7])[0] + " - " + helper_functions.getdate(class_info[6], class_info[7])[1]
        else:
            class_info[6] = class_info[8] + "s, " + helper_functions.getdate(class_info[6], class_info[7])[0] + " - " + helper_functions.getdate(class_info[6], class_info[7])[1]
    else:
        class_info[6] = "TBD"
    class_info.remove(class_info[7])
    class_info.remove(class_info[7])
    class_info.insert(2, "signup.helmlearning.com/page1.html?class=" + class_name.lower().replace(" ", "-"))
    class_info.insert(1, "[prev classes]")
    cursor.execute(sql5)
    email_info = list(cursor.fetchall()[0])

    # print(class_info)
    prep_to_send("esa", emails, email_info, class_info, qwert=qwert)
    if did_the_emails_fail_to_send[0] == True:
        return 1, did_the_emails_fail_to_send[1], did_the_emails_fail_to_send[2], 
    return 0, '"iTs FiNe. iM fInE" she said, clearly mad'

def e3(class_name, cursor):
    emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql6 = 'SELECT final_student FROM classes WHERE short_name = "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT short_name, starttime, endtime, e3_briefdescription, zoom, zoom, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="e3"'
    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"

    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    cursor.execute(sql6.format(class_name))
    last_student = cursor.fetchall()[0][0]
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        sb = cursor.fetchall()
        if len(sb) == 0:
            continue
        else:
            des_emaux = sb[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        # print(i[1])
        # print(final_student)
        # if (i[1] == last_student):
        #     print("BREAK")
        #     break
    #print(emails)
    
    class_info[1] = helper_functions.gettime(class_info[1], class_info[2])[0]
    class_info.remove(class_info[2])
    cursor.execute("SELECT recordings FROM classes WHERE short_name = '%s'" % class_name)
    try:
        recordings_folder = cursor.fetchall()[0][0]
    except:
        recordings_folder = '[will be sent by your teacher soon]'
    class_info.insert(1, recordings_folder)
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    # print(class_info)

    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0] + ",<br>The following email is an automated email about Welcome details for your class sent out to all of the students in this session of your class. (Note: You do not need to do anything with this email)<br><br>---------------------------------------------<br><br>Hello Totally Real Student"
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)

    prep_to_send("e3", emails, email_info, class_info)

def e4(class_name, cursor):
    emails = []
    #send e4
    
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT name, e4_continuingfurther, recordings, teacher, email, email, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="e4"'

    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        sb = cursor.fetchall()
        if len(sb) == 0:
            continue
        else:
            des_emaux = sb[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        # print(i[1])
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    # print(class_info[-2])
    sql6 = "UPDATE classes SET final_student = null WHERE short_name = '{}'".format(class_name)
    sql7 = "UPDATE classes SET last_student = '{}' WHERE short_name = '{}'".format(class_info[-2], class_name)
    sql8 = "UPDATE classes SET class_started = 0 WHERE short_name = '{}'".format(class_name)
    sql9 = "UPDATE classes SET day = '' WHERE short_name = '{}'".format(class_name)
    sql10 = "UPDATE classes SET startdate = '0000-00-00' WHERE short_name = '{}'".format(class_name)
    sql11 = "UPDATE classes SET enddate = '0000-00-00' WHERE short_name = '{}'".format(class_name)
    cursor.execute(sql6)
    cursor.execute(sql7)
    cursor.execute(sql8)
    cursor.execute(sql9)
    cursor.execute(sql10)
    cursor.execute(sql11)

    # FLABBERGAS

    #make sure to change the final student and the last student
    #also make sure to change the class_started
    #and the day and week
    # print(class_info)
    class_info.insert(1, class_name.replace(" ", "-"))
    class_info.insert(1, class_name.replace(" ", "-"))
    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0] + ",<br>The following email is an automated email about Welcome details for your class sent out to all of the students in this session of your class. (Note: You do not need to do anything with this email)<br><br>---------------------------------------------<br><br>Hello Totally Real Student"
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)

    prep_to_send("e4", emails, email_info, class_info)

def e4ish(class_name, cursor):
    emails = []
    #send e4
    
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT name, e4_continuingfurther, recordings, teacher, email, email, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="e4"'

    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        sb = cursor.fetchall()
        if len(sb) == 0:
            continue
        else:
            des_emaux = sb[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        # print(i[1])
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    # print(class_info[-2])
    sql6 = "UPDATE classes SET final_student = null WHERE short_name = '{}'".format(class_name)
    sql7 = "UPDATE classes SET last_student = '{}' WHERE short_name = '{}'".format(class_info[-2], class_name)
    sql8 = "UPDATE classes SET class_started = 0 WHERE short_name = '{}'".format(class_name)
    sql9 = "UPDATE classes SET day = '' WHERE short_name = '{}'".format(class_name)
    sql10 = "UPDATE classes SET startdate = '0000-00-00' WHERE short_name = '{}'".format(class_name)
    sql11 = "UPDATE classes SET enddate = '0000-00-00' WHERE short_name = '{}'".format(class_name)
    # cursor.execute(sql6)
    # cursor.execute(sql7)
    # cursor.execute(sql8)
    # cursor.execute(sql9)
    # cursor.execute(sql10)
    # cursor.execute(sql11)
    # print("Updated! ")
    #make sure to change the final student and the last student
    #also make sure to change the class_started
    #and the day and week
    # print(class_info)
    class_info.insert(1, class_name)
    class_info.insert(1, class_name)
    sql_teacher_email = "SELECT email, email,teacher FROM classes WHERE id = '{}'".format(class_id)
    cursor.execute(sql_teacher_email)
    teacher_info = list(cursor.fetchall()[0])
    emails.append(teacher_info)

def er1(class_name, cursor):
    emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT name, day, starttime, endtime, day, startdate, day, enddate, zoom, zoom, e1_additionalwork, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="er1"'
    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
        class_info[-2] = "9999-99-99 99:99:99"

    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        sb = cursor.fetchall()
        if len(sb) == 0:
            continue
        else:
            des_emaux = sb[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        # print(i[1])
    
    import datetime
    skipclass = None
    for i in skipping_weeks:
        if class_info[5] < datetime.date(i[0], i[1], i[2]) and class_info[7] > datetime.date(i[0], i[1], i[2]):
            skipclass = "5 Weeks, once per week)<br><strong>{}</strong>".format(i[3])

    if "weeklong" in class_info[1]:
        skipclass = "weeklong"
        class_info[1] = "Monday"
        class_info[4] = "Monday"
        class_info[6] = "Friday"

    est = helper_functions.gettime(class_info[2], class_info[3])[0]
    cst = helper_functions.gettime(class_info[2], class_info[3])[1]
    class_info[2] = est
    class_info[3] = cst
    stime = helper_functions.getdate(class_info[5], class_info[7])[0]
    etime = helper_functions.getdate(class_info[5], class_info[7])[1]
    class_info[5] = stime
    class_info[7] = etime
    class_info.remove(class_info[-2])
    class_info.remove(class_info[-1])
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    # print(class_info)

    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0] + ",<br>The following email is an automated email about Welcome details for your class sent out to all of the students in this session of your class. (Note: You do not need to do anything with this email)<br><br>---------------------------------------------<br><br>Hello Totally Real Student"
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)

    prep_to_send("er1", emails, email_info, class_info, qwert=[skipclass])

def er2(class_name, cursor):
    emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT short_name, zoom, zoom, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="er2"'
    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
        class_info[-2] = "9999-99-99 99:99:99"

    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        sb = cursor.fetchall()
        if len(sb) == 0:
            continue
        else:
            des_emaux = sb[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        # print(i[1])
    
    class_info.remove(class_info[-2])
    class_info.remove(class_info[-1])
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    # print(email_info[1])


    if __name__ == "__main__":
        run_class_starting = input("Run class_starting.py? ")
        if run_class_starting.lower() == "yes":
            import class_starting
            
    print("teacher email: %s" % (email_info))
    
    sql = 'SELECT id, final_student FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "{}"'
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
        # input("Good?")

    cursor.execute(sql4.format(class_name))


    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0] + ",<br>The following email is an automated email about Welcome details for your class sent out to all of the students in this session of your class. (Note: You do not need to do anything with this email)<br><br>---------------------------------------------<br><br>Hello Totally Real Student"
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)

    prep_to_send("er2", emails, email_info, class_info)

def et2_logistics(class_name, cursor):
    email_name = "et2-logistics"
    emails = []
    # sql3 = 'SELECT email, email, teacher FROM classes WHERE short_name = "{}"'
    sql4 = 'SELECT name, starttime, endtime, day, startdate, enddate FROM classes WHERE short_name = "{}"'
    #               0      1          2      3        4         5
    sql5 = 'SELECT subject, content FROM templates WHERE name="%s"' % email_name

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    # cursor.execute(sql3.format(class_name))
    # des_emaux = list(cursor.fetchall()[0])
    # des_emaux[1] = None
    # emails.append(des_emaux)
    
    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0]
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)
    
    emails = list(set(emails))
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]


    time = helper_functions.get_time_v2(class_info[1], class_info[2])
    date = helper_functions.get_date_v2(day=class_info[3], startdate=class_info[4], enddate=class_info[5])
    class_info[3] = date
    class_info.remove(class_info[5])
    class_info.remove(class_info[4])
    class_info[1] = time
    class_info.remove(class_info[2])

    prep_to_send(email_name, emails, email_info, class_info)

def et3_zoom(class_name, cursor):
    emails = []
    # sql3 = 'SELECT email, email, teacher FROM classes WHERE short_name = "{}"'
    # sql4 = 'SELECT name, starttime, endtime, day, startdate, enddate, short_name, short_name, sharing_mats, short_name, short_name, short_name, sharing_mats FROM classes WHERE short_name = "{}"'
    #               0      1          2      3        4         5        6            7           8           9          10             11          12
    sql5 = 'SELECT subject, content FROM templates WHERE name="et3-zoom"'
    sql4 = 'SELECT zoom, zoom FROM classes WHERE short_name = "{}"'
    # cursor.execute(sql4.format(class_name))
    # class_info = list(cursor.fetchall()[0])
    # if __name__ == "__main__":
    #     recordings_folder = input("What is the recordings folder link? ")
    # else:
    #     recordings_folder = "[We will send this in an upcoming email]"
    try:
        recordings_folder = create_folder(class_name)
    except:
        helper_functions.send_email("Make the %s recording folder" % class_name, "lmaoo ripp", "vikramanantha@gmail.com")
        recordings_folder = "[Will be sent soon]"
    class_info = [recordings_folder, recordings_folder]
    # cursor.execute(sql3.format(class_name))
    # des_emaux = list(cursor.fetchall()[0])
    # des_emaux[1] = None
    # emails.append(des_emaux)
    
    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0]
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)
    
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    cursor.execute(sql4.format(class_name))
    ihyfbsb = list(cursor.fetchall()[0])
    class_info.append(ihyfbsb[0])
    class_info.append(ihyfbsb[1])

    # helper_functions.send_email("Make the %s Zoom Link" % class_name, "lmaoo ripp", "vikramanantha@gmail.com")

    prep_to_send("et3-zoom", emails, email_info, class_info)

def et2_sharing(class_name, cursor):
    email_name = "et2-sharing"
    emails = []
    # sql3 = 'SELECT email, email, teacher FROM classes WHERE short_name = "{}"'
    sql4 = 'SELECT short_name, short_name, short_name, short_name, sharing_mats, sharing_mats, short_name FROM classes WHERE short_name = "{}"'
    #              0 (--)      1 (--)      2 (--)      3 (--)      4             5             6
    sql5 = 'SELECT subject, content FROM templates WHERE name="{}"'.format(email_name)

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    # cursor.execute(sql3.format(class_name))

    dashing_through_the_snow = class_info[0].replace(' ', '-').lower()
    class_info[0] = dashing_through_the_snow
    class_info[1] = dashing_through_the_snow
    class_info[2] = dashing_through_the_snow
    class_info[3] = dashing_through_the_snow

    # des_emaux = list(cursor.fetchall()[0])
    # des_emaux[1] = None
    # emails.append(des_emaux)
    
    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0]
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)
    
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]

    prep_to_send(email_name, emails, email_info, class_info)

def et3_emails(class_name, cursor):
    email_name = "et3-emails"
    emails = []
    # sql3 = 'SELECT email, email, teacher FROM classes WHERE short_name = "{}"'
    sql4 = 'SELECT short_name, short_name, name, name, name, name, name, name, short_name, name FROM classes WHERE short_name = "{}"'
    #              0 (--)      1 (--)      2     3     4     5     6     7     8           9
    sql5 = 'SELECT subject, content FROM templates WHERE name="{}"'.format(email_name)

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    # cursor.execute(sql3.format(class_name))

    dashing_through_the_snow = class_info[0].replace(' ', '-').lower()
    class_info[0] = dashing_through_the_snow
    class_info[1] = dashing_through_the_snow

    # des_emaux = list(cursor.fetchall()[0])
    # des_emaux[1] = None
    # emails.append(des_emaux)
    
    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0]
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)
    
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]

    prep_to_send(email_name, emails, email_info, class_info)

def et4_end(class_name, cursor):
    emails = []
    # sql3 = 'SELECT email, email, teacher FROM classes WHERE short_name = "{}"'
    # sql4 = 'SELECT name, starttime, endtime, day, startdate, enddate, short_name, short_name, sharing_mats, short_name, short_name, short_name, sharing_mats FROM classes WHERE short_name = "{}"'
    #               0      1          2      3        4         5        6            7           8           9          10             11          12
    sql5 = 'SELECT subject, content FROM templates WHERE name="et4-end"'
    class_name = class_name[:1].upper() + class_name[1:].lower()
    class_info = [class_name]
    # cursor.execute(sql3.format(class_name))
    # des_emaux = list(cursor.fetchall()[0])
    # des_emaux[1] = None
    # emails.append(des_emaux)
    teach_email = helper_functions.get_current_teacher_emails(class_name)
    teacher_info = ['', '', '']
    for i in teach_email:
        # cursor.execute(sql_teacher_email)
        # teacher_info = list(cursor.fetchall()[0])
        teacher_info[2] = i[0]
        teacher_info[0], teacher_info[1] = i[1], i[1]
        emails.append(teacher_info)
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    prep_to_send("et4-end", emails, email_info, class_info)

def esc(class_name, cursor):
    emails = []
    cursor.execute('SELECT id from classes where short_name = "{}"'.format(class_name))
    class_id = cursor.fetchall()[0][0]
    cursor.execute('select student_id from classes_to_students where class_id = %s and which = 10' % class_id);
    stud_ids = cursor.fetchall()
    ###### TO BE FINISHED JUNE 12 2022 #######
    for i in stud_ids:
        sid = i[0]
        cursor.execute("select Student_Name from students where id = '%s'" % sid)
        fname = cursor.fetchall()[0][0]
        cursor.execute("select Email_Address, Parent_Email from students where id = '%s'" % sid)
        stud_info = cursor.fetchall()[0]
        cursor.execute("select day, startdate, enddate from classes where short_name = '%s'" % class_name)
        class_info = cursor.fetchall()[0]
        class_details = []
        class_details.append(helper_functions.get_date_v2(*class_info))
        cursor.execute("select starttime, endtime from classes where short_name = '%s'" % class_name)
        class_info = cursor.fetchall()[0]
        class_details.append(helper_functions.get_time_v2(*class_info))
        cursor.execute("select teacher from classes where short_name = '%s'" % class_name)
        class_info = cursor.fetchall()[0]
        for j in class_info:
            class_details.append(j)
        
        encoded_id = helper_functions.encode(sid)
        synclink = "http://signup.helmlearning.com/class-signup.html?class=%s_signup&%s" % (class_name, encoded_id)
        asynclink = "http://signup.helmlearning.com/class-signup.html?class=%s_async&%s" % (class_name, encoded_id)
        subject = "Live %s session running soon! | HELM Learning" % class_name
        email = """
        Hi {}!<br>
        We see that you have shown interest in {} in the past. Lucky for you, we have a live {} class running soon. Here are the details:<br>
         - Taught by: {}<br>
         - Dates: {}<br>
         - Time: {}<br>
        <br>
        If you are interested in taking this class, <a href='{}'>click here</a>, which will sign you up for the class<br>
        <br>
        Alternatively, if you cannot make the class live on zoom, but still want to learn the content, you can receive class recordings
        and class materials once the class has ended. To receive access, <a href='{}'>click here</a>.<br>
        <br>
        Thank you so much being part of HELM Learning.<br>
        Best,<br>
        Vikram from <strong style='color: #642c94'>HELM Learning</strong><br>
        """

        email = email.format(fname, class_name, class_name, *class_details, synclink, asynclink)

        helper_functions.send_email(subject, email, *stud_info)
        print("SENT EMAIL TO %s (%s, %s)" % (fname, *stud_info))

    ###### TO BE FINISHED JUNE 13 2022--- FIX THE EMAIL WITH THE LINKS #######

def ge(class_name, cursor):
    emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql4 = 'SELECT final_student, last_student FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]
    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
        class_info[-2] = "9999-99-99 99:99:99"
    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        sb = cursor.fetchall()
        if len(sb) == 0:
            continue
        else:
            e = sb[0]
        if (list(e) not in emails):
            emails.append(list(e))
    for i in emails:
        if __name__ == "__main__":
            print(i[0])
            print(i[1])
    #input("good?")
    return emails

def prep_to_send(email_to_send, emails, email_info, class_info=[], welcome_classinfo=[], waitlist_emails=[], qwert=[None], waitlist_emailinfo=[], waitlist_classinfo=[]):
    if __name__ == "__main__":
        sbelliot = input("Test or no?")
        if sbelliot.lower() == "test":
            emails = [["dasmartone3141@gmail.com", "dasmartone3141@gmail.com", "SB. Elliot III"]]

    if (email_to_send != "e2"):
        class_info = list(class_info)
        for c in range(0, len(class_info)):
            if class_info[c] == None:
                class_info[c] = ""
    for j in emails:
        print(j)
    if __name__ == "__main__":
        input("Send?")
    for j in emails:
        print(j[0])
        if j[1] != None:
            print(j[1])
        print(j[2])
        if j[2] == "":
            continue
        if (email_to_send == "e2"):
            print("\n\n\n%s\n\n\n" % welcome_classinfo)
            send("e1", email_info[0], email_info[1], j[2], j[0], j[1], welcome_classinfo)
        else:
            if (email_to_send == "esa"):
                class_info[1] = j[3]
                
                send(email_to_send, email_info[0], email_info[1], j[2], j[0], j[1], class_info, extra_content=qwert[j[0]])
            else:
                send(email_to_send, email_info[0], email_info[1], j[2], j[0], j[1], class_info, extra_content=qwert[0])
            
    if (email_to_send == "e2"):
        for j in waitlist_emails:
            print(j)
        if __name__ == "__main__":
            input("Send??")
        for j in waitlist_emails:
            print("Waitlist")
            print(j[0])
            print(j[1])
            send(email_to_send, waitlist_emailinfo[0], waitlist_emailinfo[1], j[2], j[0], j[1], waitlist_classinfo)
    print("\nEmails not sent: ")

#tutorial at https://realpython.com/python-send-email/

if __name__ == "__main__":
    db = "HELM_Database"
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    email_to_send = input("E1, E2, E3, E4, ESA, ER1, ER2, Get Emails? ").lower()
    class_name = input("class? ").lower()
    class_name = class_name[0].upper() + class_name[1:]
    if (email_to_send == "e1"):
        e1(class_name, cursor)
    elif (email_to_send == "e2"):
        e2(class_name, cursor)
    elif (email_to_send == "e3"):
        e3(class_name, cursor)
    elif (email_to_send == "e4"):
        e4(class_name, cursor)
    elif (email_to_send == "e4ish"):
        e4ish(class_name, cursor)
    elif (email_to_send == "esa"):
        classes = []
        sbslas = input("Find similar classes the `Manual` way or the `Automatic` way? ")
        if sbslas.lower() in "manual":
            while True:
                r = input("What classes? ").lower()
                if (r == 'stop' or r == None or r== ''):
                    break
                classes.append(r[0].upper() + r[1:])
        else:
            ser = int(input("how many classes? "))
            classes = helper_functions.get_related_classes(class_name)[:ser]
        esa(class_name, cursor, classes)
    elif (email_to_send == "er1"):
        er1(class_name, cursor)
    elif (email_to_send == "er2"):
        er2(class_name, cursor)
    elif (email_to_send == "et2-logistics" or email_to_send == "et-logistics"):
        et2_logistics(class_name, cursor)
    elif (email_to_send == "et3-zoom" or email_to_send == "et-zoom"):
        et3_zoom(class_name, cursor)
    elif (email_to_send == "et2-sharing" or email_to_send == "et-sharing"):
        et2_sharing(class_name, cursor)
    elif (email_to_send == "et3-emails" or email_to_send == "et-emails"):
        et3_emails(class_name, cursor)
    elif (email_to_send == "et4-end" or email_to_send == "et-end" or email_to_send == "et4"):
        et4_end(class_name, cursor)
    elif (email_to_send == "esc"):
        esc(class_name, cursor)
    elif (email_to_send == "ge"):
        ge(class_name, cursor)
    else:
        print("You're bad and you should feel bad about yourself")
    for i in not_sent_emails:
        print(i)        
    cnx.commit()
    cursor.close()
    cnx.close()

# final student for Python 5 week class: 2020-12-05 20:26:44
# last student for Py: 2020-08-09 20:38:18

# last student: 2020-12-05 20:26:44
