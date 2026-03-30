from django.contrib import admin
from unfold.admin import ModelAdmin
from productions.models import Production, Category


# Register your models here.
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'cover_image', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Production)
class ProductionAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date_created', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured', 'date_created')
    search_fields = ('title', 'short_description', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date_created'
    filter_horizontal = ['equipment']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'date_created', 'location')
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'cover_image', 'video_url')
        }),
        ('Settings', {
            'fields': ('is_featured', )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
