from django.contrib import admin
from .models import Personal_info,USER_details
# Register your models here.
admin.site.register(USER_details)
admin.site.register(Personal_info)