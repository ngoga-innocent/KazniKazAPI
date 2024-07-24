from django.contrib import admin
from .models import MyWallet,WalletHistory,Payments
# Register your models here.
admin.site.register(MyWallet)
admin.site.register(WalletHistory)
admin.site.register(Payments)