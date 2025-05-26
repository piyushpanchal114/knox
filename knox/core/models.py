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
        ordering = ['created_at']


class Subscription(models.Model):
    """Model for Subscriptions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_subscriptions')
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name='plan_subscriptions')
    status = models.CharField(
        max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    class Meta:
        ordering = ['-start_date']


class Invoice(models.Model):
    """Model for Invoices"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name='invoices')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='invoices')
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

    class Meta:
        ordering = ['-created_at']
