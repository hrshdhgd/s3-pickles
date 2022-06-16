import os
from os.path import join, basename, isdir
import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore
import logging
from pathlib import Path

PARENT_DIR = Path(__file__).parent.parent.resolve()
RESOURCE_DIR = PARENT_DIR / "resources"
BUCKET_NAME = "ontobucket"

def upload_resource(
    resource_name:str,
    is_dir: bool,
    bucket:str = BUCKET_NAME, 
    object_name:str=None,
    extra_args={'ACL':'bucket-owner-full-control'}
    ) -> None:
    """Upload a file to an S3 bucket

    :param resource_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # s3 = boto3.resource('s3')
    # for bucket in s3.buckets.all():
    #     print(bucket.name)
    s3_client = boto3.client('s3')
    if is_dir:
        file_list = os.listdir(resource_name)
        for f in file_list:
            file_name = resource_name+"/"+f
            if object_name is None:
                object_name = basename(resource_name)+"/"+f
            try:
                response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=extra_args)
            except ClientError as e:
                logging.error(e)
                return False

    else:
        if object_name is None:
            object_name = basename(resource_name)
        try:
            response = s3_client.upload_file(resource_name, bucket, object_name, ExtraArgs=extra_args)
        except ClientError as e:
            logging.error(e)
            return False
    return True

if __name__ == "__main__":
    resource = join(RESOURCE_DIR, "bero_serial")
    upload_resource(resource, is_dir=isdir(resource))