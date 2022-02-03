from django.contrib import admin

from styleguide_example.files.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["id", "url", "file_name", "file_type", "successfully_uploaded"]

    ordering = ["-created_at"]
