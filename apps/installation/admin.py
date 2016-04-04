from django.contrib import admin
from apps.installation import models


admin.site.register(models.Port)
admin.site.register(models.Edge)
admin.site.register(models.Ship)
admin.site.register(models.Icebreaker)
admin.site.register(models.MilitaryEquipment)
