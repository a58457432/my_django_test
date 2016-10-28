from __future__ import unicode_literals

from django.db import models

class Employee(models.Model):
    name=models.CharField(max_length=20)

# Create your models here.
