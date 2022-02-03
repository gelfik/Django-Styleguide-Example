from django.urls import path

from styleguide_example.files.apis import (
    FileGeneratePresignedPostApi,
    FileLocalUploadApi,
    FileVerifyUploadApi
)

urlpatterns = [
    path(
        "generate-presigned-post/",
        FileGeneratePresignedPostApi.as_view()
    ),
    path(
        "<uuid:file_id>/local-upload/",
        FileLocalUploadApi.as_view(),
        name="local-upload"
    ),
    path(
        "<uuid:file_id>/verify-upload/",
        FileVerifyUploadApi.as_view(),
    ),
]
