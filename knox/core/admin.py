from django.contrib import admin
from .models import Plan, Subscription, Invoice


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'billing_cycle_days', 'is_active')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'user', 'plan', 'amount', 'issue_date',
                    'due_date', 'paid_date', 'status')
