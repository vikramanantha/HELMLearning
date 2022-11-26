# Vikram Anantha
# Aug 1 2021
# Uploading Files to Amazon S3


# import boto3
# import boto3.s3
# import sys
# from boto3.s3.key import Key
# import json

from helper_functions import *

bucket_name = 'helm-teacher-images'
file_name = "vikram-anantha-image.jpeg"

import logging
import boto3
from botocore.exceptions import ClientError


def main(bucket, file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
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
        
    except ClientError as e:
        logging.error(e)
        return False
    return True

# main(bucket_name, file_name)
upload_file_to_s3(bucket_name, file_name)