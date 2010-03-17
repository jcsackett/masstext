from django.contrib.admin import site

from models import PhoneNumber, CallList

site.register(PhoneNumber)
site.register(CallList)