from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

read_write = (
    ('read', 'read'),
    ('write', 'write'),
    ('all','all'),
)
class Db_instance(models.Model):
    ip = models.CharField(max_length=30)
    port = models.CharField(max_length=10)
    role =  models.CharField(max_length=30,choices=read_write,default='all')
    def __unicode__(self):
        return u'%s %s' % (self.ip, self.role)

class Db_name (models.Model):
    dbtag = models.CharField(max_length=30)
    dbname = models.CharField(max_length=30)
    instance = models.ManyToManyField(Db_instance)
    account = models.ManyToManyField(User)
    def __unicode__(self):
        return u'%s %s' % (self.dbtag, self.dbname)

class Db_account(models.Model):
    user = models.CharField(max_length=30)
    passwd = models.CharField(max_length=30)
    role =  models.CharField(max_length=30,choices=read_write,default='all')
    tags = models.CharField(max_length=30)
    dbname = models.ManyToManyField(Db_name)
    def __unicode__(self):
        return  u'%s %s' % (self.user, self.tags)
# Create your models here.