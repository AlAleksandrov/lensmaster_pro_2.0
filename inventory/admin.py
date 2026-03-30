from django.contrib import admin
from unfold.admin import ModelAdmin
from inventory.models import Equipment

# Register your models here.
@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ('brand', 'model', 'equipment_type', 'cover_image', 'internal_id', 'is_active', 'purchase_date')
    list_filter = ('equipment_type', 'is_active', 'brand', 'purchase_date')
    search_fields = ('brand', 'model', 'internal_id', 'specifications')
    readonly_fields = ('internal_id',)

    fieldsets = (
        ('Equipment Details', {
            'fields': ('brand', 'model', 'equipment_type', 'cover_image', 'internal_id')
        }),
        ('Technical Information', {
            'fields': ('specifications', 'purchase_date', 'notes')
        }),
        ('Status & Usage', {
            'fields': ('is_active', ),
        }),
    )
