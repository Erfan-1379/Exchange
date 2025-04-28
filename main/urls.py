from .views import FetchPricesAPIView, PriceHistoryAPIView
from django.urls import path

urlpatterns = [
    path("fetch/", FetchPricesAPIView.as_view()),
    path("history/<str:currency_name>/", PriceHistoryAPIView.as_view()),
]
