from rest_framework.generics import (RetrieveAPIView, ListAPIView,
                                     CreateAPIView)
from rest_framework.permissions import IsAuthenticated

from .models import Plan
from .serializers import (UserSerializer, PlanSerializer,
                          SubscriptionCreateSerializer)


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
