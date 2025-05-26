from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Plan
from .serializers import UserSerializer, PlanSerializer


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
