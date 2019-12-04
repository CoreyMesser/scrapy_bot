import boto3
import pandas as pd
import uuid
import logging
import os

from io import StringIO
from app.constants import AWSConstants as awsc


class AWSServices(object):

    def __init__(self):
        self.client = boto3.client('s3')
        self.bucket = awsc.BUCKET

    def s3_send_list(self, user_list):
        self.client.put_object(Bucket=self.bucket, Key=user_list)
