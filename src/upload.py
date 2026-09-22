import boto3
import os
import logging

from botocore.exceptions import NoCredentialsError
from boto3.exceptions import S3UploadFailedError
from progress import ProgressPercentage

logger = logging.getLogger(__name__)

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, 
                              bucket, 
                              object_name,
                              Callback=ProgressPercentage(file_name)
                            )
        print('\nIt worked!')
        return True
    except FileNotFoundError as e:
        logger.error(e)
        return False
    except NoCredentialsError as e:
        logger.error(e)
        return False
    except S3UploadFailedError as e:
        logger.error(e)
        return False
    