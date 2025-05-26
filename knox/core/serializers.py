from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from .models import Plan, Subscription, Invoice


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model"""
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'billing_cycle_days', 'features']


class SubscriptionCreateSerializer(serializers.Serializer):
    """Serializer for creating Subscription for user"""
    plan = serializers.IntegerField(write_only=True, required=True)

    def validate_plan(self, value):
        try:
            value = Plan.objects.get(id=value, is_active=True)
        except Plan.DoesNotExist:
            raise serializers.ValidationError(
                f"Plan '{value}' not found or inactive")
        user = self.context['user']
        subscription = Subscription.objects\
            .filter(Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True),
                    user=user, status='active')
        if subscription.exists():
            raise serializers.ValidationError(
                "You already have an active subscription")
        return value

    def create(self, validated_data):
        user = self.context['user']
        plan = validated_data['plan']
        return Subscription.objects.create(user=user, plan=plan)

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['detail'] = "Subscribed successfully"
        return resp


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model"""
    plan = serializers.CharField(source='plan.name', read_only=True)
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'is_active', 'start_date', 'end_date']

    def get_is_active(self, obj: Subscription):
        if obj.status == 'active' and\
             (obj.end_date is None or obj.end_date > timezone.now()):
            return True
        else:
            return False


class InvoiceListSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model"""
    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'subscription', 'amount', 'issue_date', 'due_date',
                  'paid_date', 'status']
