from django.contrib import admin

# Register your models here.
from ads.models import Ad, AdImage, AdComment


admin.site.register(Ad)
admin.site.register(AdImage)
admin.site.register(AdComment)
