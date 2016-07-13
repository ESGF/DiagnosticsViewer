from django.contrib import admin

# Register your models here.
from .models import Dataset, UserGroup, UserKey

admin.site.register(Dataset)
admin.site.register(UserGroup)
admin.site.register(UserKey)
