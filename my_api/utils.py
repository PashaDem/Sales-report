import asyncio

from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from api.models import SalePoint, Product, Purchase


def is_authenticated(func):
    """
    async decorator implemented for checking permissions
    """
    async def inner(request):
        task = asyncio.to_thread(
            lambda u: u.user.is_authenticated, request
        )  # have to use to_thread, because
        # .is_authenticated is called only fro synchronous context
        allowed = await task
        if allowed:
            result = await func(request)
            return result
        else:
            return JsonResponse(
                {"error": "To access the data you have to be authenticated"},
                headers={"status_code": "404"},
            )

    return inner


async def purchase_adding_logic(serializer):
    product_id = serializer.validated_data["product_id"]
    sale_point_id = serializer.validated_data["sale_point_id"]
    count = serializer.validated_data["count"]
    try:
        product = await Product.objects.aget(id=product_id)
        sale_point = await SalePoint.objects.aget(id=sale_point_id)
        product.sold_count += count
        await sync_to_async(lambda m: m.save())(product)
        await Purchase.objects.async_create(
            sale_point=sale_point, product=product, count=count
        )
    except Product.DoesNotExist:
        return JsonResponse({"error": "product with such id does not exist"})
    except SalePoint.DoesNotExist:
        return JsonResponse({"error": "sale point with such id does not exist"})
    return redirect(reverse("products"))


def update_sale_point(sale_point):
    """
    this func for recomputing <total_sum> field in the SalePoint model
    """
    sale_point.calculate_purchases_sum()
    sale_point.save()


async def get_best_points_queryset():
    task_list = []
    queryset = await SalePoint.objects.async_all()
    for item in queryset:
        task_list.append(sync_to_async(update_sale_point)(item))
    await asyncio.gather(*task_list)
    queryset = await SalePoint.objects.async_order_by("-total_sum")
    return queryset[:11]
