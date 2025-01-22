# from django.contrib import admin
#
# # Register your models here.
# from django.contrib import admin
# from .models import Payment, AuditLog
#
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('application', 'amount', 'payment_method', 'paid_at')
#     list_filter = ('payment_method', 'paid_at')
#
# @admin.register(AuditLog)
# class AuditLogAdmin(admin.ModelAdmin):
#     list_display = ('user', 'action', 'timestamp')
#     list_filter = ('action', 'timestamp')
#     search_fields = ('user__username', 'details')