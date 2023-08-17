from django.db import models
from django.conf import settings

# Create your models here.
class AdditionalUserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField('Geschlecht', blank=False, null=False, max_length=20)

    one_time_token = models.CharField('Einmal-Token', blank=True, null=True, max_length=256)
    token_expiry_date = models.DateTimeField('Token Ablauf Datum', blank=True, null=True)
    has_loged_in = models.BooleanField('War eingeloggt?', default=False)

    update_date = models.DateTimeField('Geändert', auto_now=True)
    creation_date = models.DateTimeField('Erstellt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "AdditionalUserInfos"

    def __str__(self):
        return self.user.username
    

class OnetimeMessage(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField('Bezeichnung', blank=True, max_length=256)
    message = models.TextField('Nachricht', blank=False, null=False, default='')
    name_of_opener = models.CharField('Öffner', blank=True, null=True, max_length=256)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    one_time_token = models.CharField('Einmal-Token', blank=False, null=False, max_length=256)
    token_expiry_date = models.DateField('Token Ablauf Datum', blank=False, null=False)
    opend = models.BooleanField('Geöffnet?', blank=False, null=False, default=False)
    open_date = models.DateTimeField('Öffnungsdatum', blank=True, null=True)
    
    update_date = models.DateTimeField('Geändert', auto_now=True)
    creation_date = models.DateTimeField('Erstellt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "OnetimeMessages"

    def __int__(self):
        return self.id


class OnetimePassword(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField('Bezeichnung', blank=True, max_length=256)
    username = models.CharField('Benutzername', blank=True, null=True, max_length=256)
    password = models.CharField('Passwort', blank=False, null=False, max_length=256)
    name_of_opener = models.CharField('Öffner', blank=True, null=True, max_length=256)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    one_time_token = models.CharField('Einmal-Token', blank=False, null=False, max_length=256)
    token_expiry_date = models.DateField('Token Ablauf Datum', blank=False, null=False)

    opend = models.BooleanField('Geöffnet?', blank=False, null=False, default=False)
    open_date = models.DateTimeField('Öffnungsdatum', blank=True, null=True)
    
    update_date = models.DateTimeField('Geändert', auto_now=True)
    creation_date = models.DateTimeField('Erstellt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "OnetimePasswords"

    def __int__(self):
        return self.id
    

class Sended_Email(models.Model):
    id = models.AutoField(primary_key=True)
    receiver_mail = models.CharField('Empfänger-Mailadresse', blank=False, max_length=200, null=False)
    sender_mail = models.CharField('Sender-Mailadresse', blank=False, max_length=200, null=False)
    content = models.TextField('Inhalt', blank=False, null=False)
    subject = models.CharField('Betreff', blank=False, max_length=200, null=False)
    error_massage = models.TextField('Error-Nachricht', blank=True, null=True)
    send_status = models.BooleanField('Gesendet')
    creation_date = models.DateTimeField('Erstellt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sended_Emails"

    def __str__(self):
        return self.receiver_mail + "_" + str(self.creation_date)


class AdminSetting(models.Model):
    id = models.AutoField(primary_key=True)

    email_user_name = models.CharField('Email-Absender-Name', blank=False, null=False, max_length=50)
    email_user = models.EmailField('Email-Absender', blank=False, null=False)
    email_password = models.CharField('Email-Absender-Passwort', blank=False, null=False, max_length=256)

    name_error_reciever = models.CharField('Email-ErrorEmpfaenger-Name', blank=False, null=False, max_length=50)
    email_error_receiver = models.EmailField('Email-ErrorEmpfaenger', blank=False, null=False)

    update_date = models.DateTimeField('Geändert', auto_now=True)
    creation_date = models.DateTimeField('Erstellt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "AdminSettings"