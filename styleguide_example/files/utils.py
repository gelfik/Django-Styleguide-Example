import pathlib

from django.urls import reverse
from django.conf import settings


def file_generate_upload_path(instance, file_name):
    extension = pathlib.Path(file_name).suffix

    return f"files/{instance.id}{extension}"


def file_generate_local_upload_url(*, file_id: str):
    api_path = reverse('api:files:local-upload', kwargs={'file_id': file_id})

    return f"{settings.SERVER_HOST_DOMAIN}{api_path}"
