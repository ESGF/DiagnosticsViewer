from django.contrib import admin

# Register your models here.
from .models import Dataset_Access, Packages, Published, Variables

admin.site.register(Dataset_Access)
admin.site.register(Packages)
admin.site.register(Published)
admin.site.register(Variables)
