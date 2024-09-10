from django.contrib import admin
from .models import Deposit


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('tx_hash', 'sender', 'amount', 'timestamp')  # Customize fields to display
