# Vikram Anantha
# Jul 29 2021
# Upload file to Google Drive Folder
# HELM Learning

from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from helper_functions import *

# parent_folder_id = '1Bxxl5KeLltVc9_ld64axJD1iKpudMtDU'
# file_path = 'unknown-31.png'
# file_name = 'unknown-31.png'

def main():
    classname = "Pineapples"

    generate_simple_flyer(classname)

    CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    cnx, cursor = start()
    cursor.execute("SELECT sharing_mats FROM classes WHERE short_name = '{}'".format(classname))
    sharingmats_drivefolder = cursor.fetchall()[0][0]
    parent_folder_id = sharingmats_drivefolder[39:-12]


    # Upload a file
    file_metadata = {
        'name': "%s Simple Flyer" % classname,
        'parents': [parent_folder_id]
    }

    media_content = MediaFileUpload("dumpsterfiles/%s_simple_flyer.png" % classname.lower().replace(" ", "-"), mimetype='image/png')

    file = service.files().create(
        body=file_metadata,

        media_body=media_content
    ).execute()

    print(file)


    # Replace Existing File on Google Drive
    # file_id = '<file id>'

    # media_content = MediaFileUpload('mp4.png', mimetype='image/png')

    # service.files().update(
    #     fileId=file_id,
    #     media_body=media_content
    # ).execute()

upload_simple_flyer("Microwave")