from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.serializers import ProductSerializer, SalePointSerializer
from api.models import Product, SalePoint


class ProductListView(generics.ListAPIView):
    """
    first requirement realization
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
