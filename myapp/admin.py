from django.contrib import admin
from myapp.models import Db_name,Db_account,Db_instance

admin.site.register(Db_name)
admin.site.register(Db_account)
admin.site.register(Db_instance)

# Register your models here.
