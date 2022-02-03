from django.utils import timezone

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from styleguide_example.files.models import File
from styleguide_example.files.services import (
    file_generate_presigned_post_data,
    file_verify_upload,
    file_local_upload
)

from styleguide_example.api.mixins import ApiAuthMixin


class FileGeneratePresignedPostApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        presigned_data = file_generate_presigned_post_data(
            request=request, **serializer.validated_data
        )

        return Response(data=presigned_data, status=status.HTTP_200_OK)


class FileLocalUploadApi(ApiAuthMixin, APIView):
    def post(self, request, file_id):
        if settings.USE_S3_UPLOAD:
            raise PermissionDenied('USE_S3_UPLOAD is enabled. Access to this API is forbidden.')

        file = get_object_or_404(File, id=file_id)

        file_local_upload(file=file, in_memory_file=request.FILES["file"])

        return Response(status=status.HTTP_201_CREATED)


class FileVerifyUploadApi(ApiAuthMixin, APIView):
    def post(self, request, file_id):
        file = get_object_or_404(File, id=file_id)

        file_verify_upload(file=file)

        return Response(status=status.HTTP_200_OK)
