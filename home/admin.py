from django.contrib import admin
from .models import AdditionalUserInfo, OnetimeMessage, OnetimePassword

# Register your models here.
class AdminAdditionalUserInfo(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'gender',
                    'update_date',
                    'creation_date',
                    ]


class AdminOnetimeMessage(admin.ModelAdmin):
    list_display = ['id',
                    'name',
                    'opend',
                    'creator',
                    'name_of_opener',
                    'message',
                    'one_time_token',
                    'token_expiry_date',
                    'update_date',
                    'creation_date',
                    ]
    

class AdminOnetimePassword(admin.ModelAdmin):
    list_display = ['id',
                    'name',
                    'opend',
                    'creator',
                    'name_of_opener',
                    'username',
                    'password',
                    'one_time_token',
                    'token_expiry_date',
                    'update_date',
                    'creation_date',
                    ]

admin.site.register(AdditionalUserInfo, AdminAdditionalUserInfo)
admin.site.register(OnetimeMessage, AdminOnetimeMessage)
admin.site.register(OnetimePassword, AdminOnetimePassword)