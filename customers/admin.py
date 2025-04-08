# Register your models here.
from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'total_spent', 'visit_count', 'last_purchase_date', 'tag', 'is_active')
    list_filter = ('city', 'tag', 'is_active')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-updated_at',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'email', 'address', 'city', 'state', 'pincode', 'tag', 'is_active')
        }),
        ('Stats', {
            'fields': ('total_spent', 'visit_count', 'last_purchase_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
