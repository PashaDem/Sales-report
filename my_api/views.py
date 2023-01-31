from asgiref.sync import sync_to_async
from django.http import JsonResponse

from api.models import Product, SalePoint
from api.serializers import (
    ProductSerializer,
    SalePointSerializer,
    PurchaseAddingSerializer,
    BestSalePointSerializer,
    BestProductSerializer,
)
from my_api.utils import (
    is_authenticated,
    get_best_points_queryset,
    purchase_adding_logic,
)


@is_authenticated
async def get_product_list(request):
    products = await Product.objects.async_all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)


@is_authenticated
async def get_sale_point_list(request):
    sale_points = await SalePoint.objects.async_all()
    serializer = SalePointSerializer(sale_points, many=True)
    result = await sync_to_async(lambda m: m.data)(serializer)
    return JsonResponse(result, safe=False)


@is_authenticated
async def add_purchase(
    request,
):  # this view does not work because the csrf logic is blocked
    if request.method == "POST":
        serializer = await sync_to_async(lambda r: PurchaseAddingSerializer(r.data))(
            request
        )
        valid = sync_to_async(lambda data: data.is_valid())(serializer)
        if valid:
            result = await purchase_adding_logic(serializer)
            return result
        else:
            return JsonResponse(
                {
                    "error": "The data you sent is invalid. Get in touch with documentation"
                },
                headers={"status_code": "404"},
            )
    else:
        return JsonResponse(
            {"error": "This method is not allowed"}, headers={"status_code": 405}
        )


@is_authenticated
async def get_best_points(request):
    sale_points = await get_best_points_queryset()
    serializer = BestSalePointSerializer(sale_points, many=True)
    return JsonResponse(serializer.data, safe=False)


@is_authenticated
async def get_best_products(request):
    products = await Product.objects.async_order_by("-sold_count")
    products = products[:11]
    serializer = BestProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)
