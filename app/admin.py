from app.models import *
from django.contrib import admin
from solo.admin import SingletonModelAdmin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/payment_change_list.html'
    list_display = ('bot_user', 'amount', 'payment_date', 'tariff', 'payed')
    list_filter = ('payed', 'payment_date')
    search_fields = ('bot_user__name',)
    ordering = ('-payment_date',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'tariff', 'UZS', 'RUB', 'USD', 'XTR')
    list_display_links = None
    list_filter = ('tariff',)
    search_fields = ('tariff',)
    fields = ('tariff', 'UZS', 'RUB', 'USD', 'XTR')
    ordering = ('tariff',)
    list_editable = ('tariff', 'UZS', 'RUB', 'USD', 'XTR')
