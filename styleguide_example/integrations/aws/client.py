import logging

import boto3
from botocore.exceptions import ClientError

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from typing import Optional


def s3_get_client():
    required_config = [
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.AWS_STORAGE_BUCKET_NAME,
    ]

    if not all(required_config):
        raise ImproperlyConfigured(f'AWS not configured.')

    return boto3.client(
        service_name="s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def s3_generate_presigned_post(*, file_path: str, file_type: str) -> Optional[str]:
    s3_client = s3_get_client()

    try:
        url = s3_client.generate_presigned_post(
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path,
            Fields={"acl": settings.AWS_DEFAULT_ACL, "Content-Type": file_type},
            Conditions=[{"acl": settings.AWS_DEFAULT_ACL}, {"Content-Type": file_type}],
            ExpiresIn=settings.AWS_FILES_EXPIRY,
        )

    except ClientError as e:
        logging.error(e)
        return None

    return url
