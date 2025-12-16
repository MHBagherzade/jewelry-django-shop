from django.contrib import admin
from .models import GoldPriceHistory, TabloSettings

@admin.register(GoldPriceHistory)
class GoldPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'gold_18_carat', 'coin_emami', 'currency_usd')
    list_filter = ('date',)
    search_fields = ('date',)
    ordering = ('-date',)

@admin.register(TabloSettings)
class TabloSettingsAdmin(admin.ModelAdmin):
    list_display = ('auto_update', 'update_interval_minutes', 'last_update', 'api_enabled')