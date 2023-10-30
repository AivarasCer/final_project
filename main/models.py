from django.db import models
from django.contrib.auth.models import User


class MetaData(models.Model):
    name = models.CharField(null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    upload_at = models.DateField(null=True)
    processing_time = models.TimeField(null=True)
    chars = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name} {self.user} {self.upload_at} {self.processing_time} {self.chars}'
