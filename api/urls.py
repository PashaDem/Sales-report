from django.urls import path
from api.views import ProductListView, SalePointListView


urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("sale_points/", SalePointListView.as_view()),
]
