from flask_sqlalchemy import SQLAlchemy
import boto3

class S3Wrapper:
    def __init__(self):
        self.s3 = None
        self.bucket_name = None
    def init(self, access_key, secret_key, region, bucket_name):
        self.s3 = boto3.client(
            's3', 
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key, 
            region_name=region
        )
        self.bucket_name = bucket_name

db = SQLAlchemy()
s3_wrapper = S3Wrapper()

