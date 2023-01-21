from django.urls import path
from api.views import (
    ProductListView,
    SalePointListView,
    BestSalePointView,
    add_purchase_view,
    BestSoldProductsView,
)


urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("sale_points/", SalePointListView.as_view()),
    path("best_sale_points/", BestSalePointView.as_view()),
    path("best_sold_products/", BestSoldProductsView.as_view()),
    path("add_purchase/", add_purchase_view),
]
