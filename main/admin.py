from django.contrib import admin
from .models import MetaData


class MetaDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'upload_at', 'chars', 'file_type')
    # search_fields = ('name', 'user')


admin.site.register(MetaData)
