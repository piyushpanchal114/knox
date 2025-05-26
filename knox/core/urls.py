from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.ProfileRetrieveAPIView.as_view(), name="profile"),
    path("plans/", views.PlanListAPIView.as_view(), name="plans"),
    path("subscribe/",
         views.UserSubscriptionCreateAPIView.as_view(), name="subscribe"),
    path("unsubscribe/",
         views.UserUnsubscribeAPIView.as_view(), name="unsubscribe"),
    path("invoices/",
         views.UserInvoiceListAPIView.as_view(), name="invoices"),
]
