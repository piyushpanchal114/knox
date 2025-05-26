from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import (RetrieveAPIView, ListAPIView,
                                     CreateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plan, Subscription, Invoice
from .serializers import (UserSerializer, PlanSerializer,
                          SubscriptionCreateSerializer, InvoiceListSerializer)


class ProfileRetrieveAPIView(RetrieveAPIView):
    """Retrieve the current user's profile."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PlanListAPIView(ListAPIView):
    """List all active plans."""
    permission_classes = [IsAuthenticated]
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)


class UserSubscriptionCreateAPIView(CreateAPIView):
    """Create user's subscription."""
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        return context


class UserUnsubscribeAPIView(APIView):
    """Cancel user's subscription."""
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        subscription = Subscription.objects.filter(
            Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True),
            user=request.user, status='active').first()
        if not subscription:
            return Response(
                {"message": "You do not have an active subscription"},
                status=status.HTTP_400_BAD_REQUEST)
        subscription.status = 'cancelled'
        subscription.end_date = timezone.now()
        subscription.save()
        return Response({"message": "Your subscription has been cancelled"},
                        status=status.HTTP_200_OK)


class UserInvoiceListAPIView(ListAPIView):
    """List user's invoices"""
    serializer_class = InvoiceListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects\
            .select_related('subscription', 'subscription__plan')\
            .filter(user=self.request.user)
