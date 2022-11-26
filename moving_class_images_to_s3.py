# Vikram Anantha
# Sept 4 2021
# Moving Class Images to s3
# HELM Learning

import numpy
import mysql.connector
from mysql.connector import errorcode
from helper_functions import *
import pandas as pd

cnx, cursor = start()
cursor.execute("SELECT short_name FROM classes")
classes = cursor.fetchall()
for i in classes:
    short_name = i[0]


    try:
        upload_file_to_s3("helm-class-images", "/Users/vikramanantha/Downloads/Class Images/" + short_name.lower().replace(" ", "-") + '-image.png', short_name.lower().replace(" ", "-") + "-image.png")
    except:
        input("Praveeeeen!!!! Change the file name to be %s " % (short_name.lower().replace(" ", "-") + "-image.png"))
        upload_file_to_s3("helm-class-images", "/Users/vikramanantha/Downloads/Class Images/" + short_name.lower().replace(" ", "-") + '-image.png', short_name.lower().replace(" ", "-") + "-image.png")
    cursor.execute("UPDATE classes SET icon = '{}' WHERE short_name = '{}'".format(
        'https://helm-class-images.s3.amazonaws.com/' + short_name.lower().replace(" ", "-") + "-image.png",
        short_name
        ))
    print("UPLOADED %s IMAGE\n" % short_name)





stop(cnx, cursor)