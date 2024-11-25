from django.db import models


class Price(models.Model):
    UZS = models.FloatField(null=True, blank=False, verbose_name="So'm")
    RUB = models.FloatField(null=True, blank=False, verbose_name="Рубль")
    USD = models.FloatField(null=True, blank=False, verbose_name="USD")
    XTR = models.FloatField(null=True, blank=False, verbose_name="XTR")
