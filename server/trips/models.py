from django.db import models

from auth.models import User


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    comment = models.TextField(default='', blank=True)
    user = models.ForeignKey(User, related_name='trips')
