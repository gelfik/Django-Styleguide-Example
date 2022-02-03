from config.env import env

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

USE_S3_UPLOAD = env("USE_S3_UPLOAD", default=False)

if USE_S3_UPLOAD:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

    AWS_FILES_EXPIRY = env("AWS_FILES_EXPIRY", default=60 * 60)
    AWS_S3_FILE_OVERWRITE = env("AWS_S3_FILE_OVERWRITE", default=False)
    AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL", default='public-read')

    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default=None)
    AWS_S3_DOMAIN = (
        AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    )
    MEDIA_URL = f"https://{AWS_S3_DOMAIN}/media/"
