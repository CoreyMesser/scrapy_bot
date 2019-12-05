import boto3
from datetime import datetime
from app.constants import AWSConstants as awsc

class AWSServices(object):

    def __init__(self):
        self.client = boto3.client('s3')
        self.bucket = awsc.BUCKET

    def s3_send_list(self, csv_file):
        self.client.put_object(Bucket=self.bucket, Key=csv_file)

    def s3_list_objects(self):
        return self.client.list_objects()

    def datetime_now_str(self):
        return ''.join(''.join(str(datetime.now()).split(' ')).split('.'))


    def assemble_s3_path_twitter(self):
        return 's3://' + self.bucket + awsc.TWITTER + self.datetime_now_str() + '.csv'


