from django.db import models
from django.contrib.auth.models import User


class MetaData(models.Model):
    name = models.CharField(max_length=20, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    upload_at = models.DateField(null=True)
    file_type = models.CharField(max_length=6, null=True)

    def __str__(self):
        return f'{self.upload_at} {self.user} - {self.name}'
