from django.contrib import admin
from .models import AdditionalUserInfo

# Register your models here.
class AdminAdditionalUserInfo(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'gender',
                    'update_date',
                    'creation_date',
                    ]

admin.site.register(AdditionalUserInfo, AdminAdditionalUserInfo)