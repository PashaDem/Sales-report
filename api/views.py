from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Product, SalePoint, Purchase
from api.serializers import (
    ProductSerializer,
    SalePointSerializer,
    BestSalePointSerializer,
    BestProductSerializer,
    PurchaseAddingSerializer,
)


class ProductListView(generics.ListAPIView):
    """
    first requirement implementation
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.all()


class SalePointListView(generics.ListAPIView):
    """
    second requirement implementation
    """

    serializer_class = SalePointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SalePoint.objects.all()


class BestSalePointView(generics.ListAPIView):
    """
    forth requirement implementation
    """

    serializer_class = BestSalePointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # initializing total_sum SalePoint's field through loop
        for item in SalePoint.objects.all():
            item.calculate_purchases_sum()
            item.save()

        return SalePoint.objects.order_by("-total_sum")[:11]


class BestSoldProductsView(generics.ListAPIView):
    """
    forth requirement implementation
    """

    serializer_class = BestProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.order_by("-sold_count")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_purchase_view(request):
    """
    third requirement implementation
    """
    serializer = PurchaseAddingSerializer(data=request.data)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data["product_id"]
        sale_point_id = serializer.validated_data["sale_point_id"]
        count = serializer.validated_data["count"]
        print(type(product_id))
        try:
            product = Product.objects.get(id=product_id)
            sale_point = SalePoint.objects.get(id=sale_point_id)
            product.sold_count += count
            product.save()
            Purchase.objects.create(sale_point=sale_point, product=product, count=count)
        except Product.DoesNotExist:
            return Response({"error": "product with such id does not exist"})
        except SalePoint.DoesNotExist:
            return Response({"error": "sale point with such id does not exist"})
        return redirect(reverse("product_list"))
    else:
        return Response(
            {"error": "The data you sent is invalid. Get in touch with documentation"},
            headers={"status_code": "404"},
        )
