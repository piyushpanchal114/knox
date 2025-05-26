import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .choice_constants import (PLAN_TYPE_CHOICES, SUBSCRIPTION_STATUS_CHOICES,
                               INVOICE_STATUS_CHOICES)


class Plan(models.Model):
    """Model for Plans"""
    name = models.CharField(
        max_length=20, choices=PLAN_TYPE_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle_days = models.IntegerField(default=30)  # Monthly by default
    features = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Subscription(models.Model):
    """Model for Subscriptions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_subscriptions')
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name='plan_subscriptions')
    status = models.CharField(
        max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def is_active(self):
        return self.status == 'active' and\
            (not self.end_date or self.end_date > timezone.now())

    def cancel(self):
        self.status = 'cancelled'
        self.end_date = timezone.now()
        self.save()

    class Meta:
        ordering = ['-start_date']


class Invoice(models.Model):
    """Model for Invoices"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name='invoices')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='invoices')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateTimeField()
    due_date = models.DateTimeField()
    paid_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=INVOICE_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.user.username} - ${self.amount}"

    def is_overdue(self):
        return self.status == 'pending' and self.due_date < timezone.now()

    def mark_paid(self):
        self.status = 'paid'
        self.paid_date = timezone.now()
        self.save()

    class Meta:
        ordering = ['-created_at']
