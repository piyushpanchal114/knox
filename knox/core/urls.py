from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.ProfileRetrieveAPIView.as_view(), name="profile"),
]
