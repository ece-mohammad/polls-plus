from django.contrib import admin

# Register your models here.
from ads.models import Ad, AdComment

admin.site.register(Ad)
admin.site.register(AdComment)
