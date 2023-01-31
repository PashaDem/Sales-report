from django.urls import path
from .views import (
    get_product_list,
    get_sale_point_list,
    add_purchase,
    get_best_points,
    get_best_products,
)

urlpatterns = [
    path("products/", get_product_list, name="products"),
    path("sale_points/", get_sale_point_list),
    path(
        "add_purchase/",
        add_purchase,
    ),  # doesn't work
    path("best_sale_points/", get_best_points),
    path("get_best_products/", get_best_products),
]
