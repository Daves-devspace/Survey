from django.contrib import admin
from django.utils.html import format_html
from .models import Client, Surveyor, Transaction, Payment

# Custom Admin Classes
admin.site.site_header = 'Great Investment Ltd.'
admin.site.site_title = 'Manage GIL'

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'lastname', 'email', 'phone', 'status', 'action', 'view_details_button')
    search_fields = ('username', 'firstname', 'lastname', 'email', 'phone')
    list_filter = ('status',)
    list_per_page = 30

    def view_details_button(self, obj):
        return format_html('<a href="/admin/Surveyor/client/{}/change/" class="button">View Details</a>', obj.id)
    view_details_button.short_description = 'View Details'
    view_details_button.allow_tags = True

@admin.register(Surveyor)
class SurveyorAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'lastname', 'email', 'phone', 'status',  'view_details_button')
    search_fields = ('username', 'firstname', 'lastname', 'email', 'phone')
    list_filter = ('status',)
    list_per_page = 35

    def view_details_button(self, obj):
        return format_html('<a href="/admin/Surveyor/surveyor/{}/change/" class="button">View Details</a>', obj.id)
    view_details_button.short_description = 'View Details'
    view_details_button.allow_tags = True

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'surveyor', 'status', 'action', 'transaction_date')
    search_fields = ('client__username', 'surveyor__username', 'status')
    list_filter = ('status', 'transaction_date')
    date_hierarchy = 'transaction_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('merchant_request_id', 'checkout_request_id', 'code', 'amount', 'status', 'transaction_date', 'action')
    search_fields = ('merchant_request_id', 'checkout_request_id', 'code', 'status')
    list_filter = ('status', 'transaction_date')
    date_hierarchy = 'transaction_date'