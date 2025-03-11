from django.contrib import admin

from user_management.models import Interest, Message, Registration

# Register your models here.
admin.site.register(Registration)
admin.site.register(Message)
admin.site.register(Interest)