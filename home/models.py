from django.db import models
from django.conf import settings

# Create your models here.
class AdditionalUserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField('Geschlecht', blank=False, null=False, max_length=20)

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