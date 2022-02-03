from typing import Dict

from django.conf import settings
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile

from styleguide_example.files.models import File
from styleguide_example.files.utils import (
    file_generate_upload_path,
    file_generate_local_upload_url
)

from styleguide_example.integrations.aws.client import s3_generate_presigned_post

from styleguide_example.users.models import BaseUser


def file_create_for_upload(*, user: BaseUser, file_name: str, file_type: str) -> File:
    file = File(
        file=None,
        file_name=file_name,
        file_type=file_type,
        uploaded_by=user,
    )
    file.full_clean()
    file.save()

    return file


@transaction.atomic
def file_generate_presigned_post_data(*, request, file_name: str, file_type: str) -> Dict:
    user = request.user

    file = file_create_for_upload(user=user, file_name=file_name, file_type=file_type)

    if settings.USE_S3_UPLOAD:
        upload_path = file_generate_upload_path(file, file.file_name)

        presigned_data = s3_generate_presigned_post(
            file_path=upload_path, file_type=file.file_type
        )

        """
        Setting the file.file path to be the s3 upload path without uploading the file.
        The actual file upload will be done by the FE.
        """
        file.file = file.file.field.attr_class(file, file.file.field, upload_path)
        file.save()
    else:
        presigned_data = {
            "url": file_generate_local_upload_url(file_id=file.id),
        }

    return {"identifier": file.id, **presigned_data}


def file_verify_upload(*, file: File) -> File:
    file.successfully_uploaded = True

    file.full_clean()
    file.save()

    return file

def file_local_upload(*, file: File, in_memory_file: InMemoryUploadedFile) -> File:
    file.file = in_memory_file

    file.full_clean()
    file.save()

    return file
