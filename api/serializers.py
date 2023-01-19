from rest_framework.serializers import ModelSerializer
from api.models import Product, SalePoint


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "description", "cost")


class SalePointSerializer(ModelSerializer):
    class Meta:
        model = SalePoint
        fields = ("address", "description", "administrators")
