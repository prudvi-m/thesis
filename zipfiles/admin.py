from django.contrib import admin
from .models import Zipfile, myuploadfile

# Register your models here.
admin.site.register(Zipfile)
admin.site.register(myuploadfile)
