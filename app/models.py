from django.db import models
from django.utils import timezone
from asgiref.sync import sync_to_async


class Price(models.Model):
    tariff = models.CharField(null=True, max_length=255, verbose_name='Тариф')
    UZS = models.FloatField(null=True, blank=False, verbose_name="So'm")
    RUB = models.FloatField(null=True, blank=False, verbose_name="Рубль")
    USD = models.FloatField(null=True, blank=False, verbose_name="USD")
    XTR = models.FloatField(null=True, blank=False, verbose_name="XTR")

    def __str__(self) -> str:
        return self.tariff

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"


class Payment(models.Model):
    bot_user = models.ForeignKey(
        "bot.Bot_user", null=True, on_delete=models.CASCADE, verbose_name="Пользователь бота"
    )
    amount = models.BigIntegerField(null=True, verbose_name="Сумма")
    currency = models.CharField(
        null=True, max_length=16, verbose_name='Валюта')
    payment_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата платежа")
    payed = models.BooleanField(default=False, verbose_name="Оплачено?")
    payment_system = models.CharField(
        null=True, blank=True, max_length=32, verbose_name="Платежная система"
    )
    tariff = models.ForeignKey(Price, null=True, on_delete=models.PROTECT)

    @property
    @sync_to_async
    def get_bot_user(self):
        return self.bot_user

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Платежи"
