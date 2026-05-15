from django.contrib import admin
from .models import Drawing, LottoPurchase, WinRecord


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ('draw_number', 'draw_date', 'numbers_display', 'bonus', 'is_completed')
    list_filter  = ('is_completed',)
    ordering     = ('-draw_number',)


@admin.register(LottoPurchase)
class LottoPurchaseAdmin(admin.ModelAdmin):
    list_display  = ('user', 'drawing', 'numbers', 'purchase_type', 'purchased_at')
    list_filter   = ('purchase_type', 'drawing')
    search_fields = ('user__username',)


@admin.register(WinRecord)
class WinRecordAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'rank', 'prize_amount', 'confirmed_at')
    list_filter  = ('rank',)
