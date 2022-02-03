import uuid

from django.db import models
from django.conf import settings

from styleguide_example.common.models import BaseModel

from styleguide_example.users.models import BaseUser

from styleguide_example.files.utils import file_generate_upload_path


class File(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=file_generate_upload_path, null=True, blank=True)

    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)

    uploaded_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

    successfully_uploaded = models.BooleanField(default=False)

    @property
    def url(self):
        if not self.successfully_uploaded:
            return ''

        if settings.USE_S3_UPLOAD:
            return self.file.url

        return f"{settings.SERVER_HOST_DOMAIN}{self.file.url}"
