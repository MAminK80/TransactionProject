from django.contrib import admin
from . import models


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'slug']
    prepopulated_fields = {'slug': ['user']}


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['seller', 'charge', 'withdraw', 'slug']
    prepopulated_fields = {'slug': ['seller']}


admin.site.register(models.Sell)
