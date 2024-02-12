# yourapp/admin.py

from django.contrib import admin
from .models import *


class customUserDisplay(admin.ModelAdmin):
    list_display = ('username', 'user_type')

admin.site.register(Custom_User, customUserDisplay)