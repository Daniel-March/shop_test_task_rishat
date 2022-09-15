from django.http import HttpRequest, JsonResponse

from shop.models import Item, Basket


def add_item_to_basket(request: HttpRequest, id: int):
    csrftoken = request.COOKIES.get("csrftoken")
    if not (basket_filter := Basket.objects.filter(customer_session=csrftoken)).exists():
        Basket(customer_session=csrftoken).save()
    basket = basket_filter.first()

    item = Item.objects.get(id=id)
    basket.items.add(item)

    return JsonResponse({}, status=200)


def remove_item_from_basket(request: HttpRequest, id: int):
    csrftoken = request.COOKIES.get("csrftoken")
    if (basket_filter := Basket.objects.filter(customer_session=csrftoken)).exists():
        basket = basket_filter.first()
        item = Item.objects.get(id=id)
        if basket.items.filter(id=item.id).exists():
            basket.items.remove(item)

    return JsonResponse({}, status=200)
