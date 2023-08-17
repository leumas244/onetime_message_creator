from django.contrib import admin
from .models import AdditionalUserInfo, OnetimeMessage, OnetimePassword, Sended_Email, AdminSetting

# Register your models here.
class AdminAdditionalUserInfo(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'gender',
                    'one_time_token',
                    'token_expiry_date',
                    'has_loged_in',
                    'update_date',
                    'creation_date',
                    ]


class AdminOnetimeMessage(admin.ModelAdmin):
    list_display = ['id',
                    'name',
                    'opend',
                    'open_date',
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
                    'open_date',
                    'creator',
                    'name_of_opener',
                    'username',
                    'password',
                    'one_time_token',
                    'token_expiry_date',
                    'update_date',
                    'creation_date',
                    ]
    

class AdminSended_Email(admin.ModelAdmin):
    list_display = ['id',
                    'receiver_mail',
                    'sender_mail',
                    'content',
                    'subject',
                    'error_massage',
                    'send_status',
                    'creation_date',
                    ]


class AdminAdminSetting(admin.ModelAdmin):
    list_display = ['id',
                    'email_user_name',
                    'email_user',
                    'name_error_reciever',
                    'email_error_receiver',
                    'update_date',
                    'creation_date',
                    ]

admin.site.register(AdditionalUserInfo, AdminAdditionalUserInfo)
admin.site.register(OnetimeMessage, AdminOnetimeMessage)
admin.site.register(OnetimePassword, AdminOnetimePassword)
admin.site.register(Sended_Email, AdminSended_Email)
admin.site.register(AdminSetting, AdminAdminSetting)