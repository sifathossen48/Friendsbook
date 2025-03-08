from django.contrib import admin

from user_management.models import Message, Registration

# Register your models here.
admin.site.register(Registration)
admin.site.register(Message)