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