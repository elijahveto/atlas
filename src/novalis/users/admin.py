from django.contrib import admin
from .models import Company, User

admin.site.register(User)
admin.site.register(Company)