import uuid

from django.db import models


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_exchanger = models.BooleanField(default=False)

class Req(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    bank = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    req = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class Invoice(models.Model):
    uniq_id = models.CharField(max_length=5, unique=True, blank=True, null=True)
    amount = models.IntegerField()
    is_complete = models.BooleanField(default=False)
    changer = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    withdrawed = models.BooleanField(default=False)
    with_course = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.uniq_id:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        return str(uuid.uuid4().hex[:10]).upper()


class Course(models.Model):
    kzt_course = models.FloatField()