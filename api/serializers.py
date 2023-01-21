from rest_framework import serializers as s
from api.models import Product, SalePoint


class ProductSerializer(s.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "cost")


class SalePointSerializer(s.ModelSerializer):
    class Meta:
        model = SalePoint
        fields = ("address", "description", "administrators")


class BestSalePointSerializer(s.ModelSerializer):
    class Meta:
        model = SalePoint
        fields = ("id", "address", "total_sum")


class BestProductSerializer(s.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "sold_count")


class PurchaseAddingSerializer(s.Serializer):
    product_id = s.IntegerField()
    sale_point_id = s.IntegerField()
    count = s.IntegerField()
