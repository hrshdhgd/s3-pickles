
from os.path import join, basename
import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore
import logging
from pathlib import Path

PARENT_DIR = Path(__file__).parent.parent.resolve()
RESOURCE_DIR = PARENT_DIR / "resources"

def upload_file_to_s3(
    file_name:str, 
    bucket:str = "ontobucket", 
    object_name:str=None,
    extra_args={'ACL':'bucket-owner-full-control'}
    ) -> None:
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # s3 = boto3.resource('s3')
    # for bucket in s3.buckets.all():
    #     print(bucket.name)

    if object_name is None:
        object_name = basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=extra_args)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    resource = join(RESOURCE_DIR, "README.md")
    upload_file_to_s3(resource)