# Vikram Anantha
# May 2 2020
# Creating the Recording Folders with a Google Drive API
# Tutorial: https://www.youtube.com/watch?v=1y0-IfRW114&t=321s
# HELM Learning

from Google import Create_Service
import pytz
import datetime
from helper_functions import *


def create_folder(class_name):
    cnx, cursor = start()
    cursor.execute("SELECT startdate, enddate FROM classes WHERE short_name = '{}'".format(class_name))
    sbell = cursor.fetchall()[0]
    startdate_bleep_bloop = sbell[0]
    enddate_bleep_bloop = sbell[1]
    sbe = getdate(startdate_bleep_bloop, enddate_bleep_bloop)
    startdate = sbe[0]
    enddate = sbe[1]

    cursor.execute("SELECT email FROM classes WHERE short_name = '{}'".format(class_name))
    teacheremail = cursor.fetchall()[0][0]

    CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    parent_id = '1uuh9sHO-5KOwJdlx0zGrhED_5bRwz737'
    file_metadata = {
        'name': '%s | %s - %s' % (class_name, startdate, enddate),
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ['1uuh9sHO-5KOwJdlx0zGrhED_5bRwz737']
    }
    folder = service.files().create(body=file_metadata).execute()
    folder_id = folder.get('id')
    # print("The Folder ID for this is %s" % file.get('id'))

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))

    batch = service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': teacheremail
    }
    batch.add(service.permissions().create(
            fileId=folder_id,
            body=user_permission,
            fields='id',
    ))
    domain_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    batch.add(service.permissions().create(
            fileId=folder_id,
            body=domain_permission,
            fields='id',
    ))
    batch.execute()
    link = 'https://drive.google.com/drive/folders/%s?usp=sharing' % folder_id

    cursor.execute("SELECT recordings FROM classes WHERE short_name = '%s'" % class_name)
    reco_folder_alr_there = cursor.fetchall()
    try:
        print("There is already an existing folder: %s" % (reco_folder_alr_there[0][0]+''))
        if __name__ == '__main__':
            ightimmaheadout = input("Are you sure you want to add a new folder? (y/n) ")
            if ightimmaheadout == "n":
                return reco_folder_alr_there[0][0]
    except:
        print("There is no folder already there!")
    # if reco_folder_alr_there[0][0] == None and __name__ == '__main__':
    #     print("There is already an existing folder: %s" % (reco_folder_alr_there[0][0]+''))
    #     input("Are you sure you want to add a new folder?")
    cursor.execute("UPDATE classes SET recordings = '%s' WHERE short_name = '%s'" % (link, class_name))
    stop(cnx=cnx, cursor=cursor)
    return link

if __name__ == '__main__':
    class_name = input("Which class do you want to create a folder for? ")
    folder_link = create_folder(class_name)
    print("\nClass Recordings Folder link is: %s" % folder_link)