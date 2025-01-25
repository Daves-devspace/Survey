from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Client, Surveyor, Payment

# Custom Admin Classes
admin.site.site_header = 'Great Investment Ltd.'
admin.site.site_title = 'Manage GIL'

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'lastname', 'email', 'phone','status', 'action_button')
    search_fields = ('username', 'firstname', 'lastname', 'email', 'phone')
    list_filter = ('username',)
    list_per_page = 30

    def action_button(self, obj):
        return format_html(
            '<a href="{}" class="btn btn-outline-dark btn-sm">View Details</a>',
            reverse('client_view_details', args=[obj.id])
        )
    action_button.short_description = 'Action'
    action_button.allow_tags = True


@admin.register(Surveyor)
class SurveyorAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'lastname', 'email', 'phone', 'status', 'action_button')
    search_fields = ('username', 'firstname', 'lastname', 'email', 'phone')
    list_filter = ('status', 'is_registered', 'is_serving')
    list_per_page = 30

    def action_button(self, obj):
        return format_html(
            '<a href="{}" class="btn btn-outline-dark btn-sm">View Details</a>',
            reverse('surveyor_view_details', args=[obj.id])
        )

    action_button.short_description = 'Action'
    action_button.allow_tags = True

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone_number', 'amount', 'transaction_date', 'status', 'action_button')
    search_fields = ('client_name', 'phone_number')  # Add phone_number to search fields
    list_filter = ('status',)  # Add phone_number to filters if needed
    list_per_page = 30

    def action_button(self, obj):
        return format_html(
            '<a href="{}" class="btn btn-outline-dark btn-sm">Check Status</a>',
            reverse('payment_details', args=[obj.id])
        )
    action_button.short_description = 'Action'
    action_button.allow_tags = True