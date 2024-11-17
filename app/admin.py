from app.models import *
from django.contrib import admin
from solo.admin import SingletonModelAdmin

admin.site.register(Price, SingletonModelAdmin)