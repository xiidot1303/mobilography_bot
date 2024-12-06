from app.models import *
from django.contrib import admin
from solo.admin import SingletonModelAdmin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/payment_change_list.html'
    list_display = ('bot_user', 'amount', 'payment_date', 'payed')
    list_filter = ('payed', 'payment_date')
    search_fields = ('bot_user__name',)
    ordering = ('-payment_date',)


admin.site.register(Price, SingletonModelAdmin)
