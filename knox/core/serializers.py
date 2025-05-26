from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Plan


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['name', 'price', 'billing_cycle_days', 'features']
