from django.contrib import admin
from .models import User,Device,Notifications,OTP
# from fcm_django.models import FCMDevice
# Register your models here.
admin.site.register(User)
admin.site.register(Device)
admin.site.register(Notifications)
admin.site.register(OTP)
# admin.site.register(FCMDevice)