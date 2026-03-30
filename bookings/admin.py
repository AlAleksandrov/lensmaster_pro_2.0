from django.contrib import admin
from unfold.admin import ModelAdmin
from bookings.models import ServicePackage, BookingRequest


# Register your models here.
@admin.register(ServicePackage)
class ServicePackageAdmin(ModelAdmin):
    list_display = ('name', 'price', 'duration_hours', 'max_photos_included', 'is_active')
    list_filter = ('is_active', 'duration_hours',)
    search_fields = ('name', 'description')

    fieldsets = (
        ('Package Details', {
            'fields': ('name', 'description', 'price')
        }),
        ('Service Specifications', {
            'fields': ('duration_hours', 'max_photos_included')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(BookingRequest)
class BookingRequestAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'event_date', 'package', 'status', 'heard_from', 'created_at')
    list_filter = ('status', 'heard_from', 'event_date', 'created_at')
    search_fields = ('first_name', '','email', 'phone', 'city', 'message')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'event_date'

    fieldsets = (
        ('Client Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'city')
        }),
        ('Event Details', {
            'fields': ('event_date', 'package', 'message')
        }),
        ('Marketing & Status', {
            'fields': ('heard_from', 'status')
        }),
        ('Internal', {
            'fields': ('internal_notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
