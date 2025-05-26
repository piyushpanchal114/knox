from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.ProfileRetrieveAPIView.as_view(), name="profile"),
    path("plans/", views.PlanListAPIView.as_view(), name="plans"),
]
