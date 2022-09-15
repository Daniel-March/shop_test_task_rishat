import uuid
from typing import List

from django.http import HttpRequest
from django.shortcuts import render, redirect

from shop.models import Item, Order, Currency, Basket
from shop.stripe import get_stripe_checkout_session


def main(request: HttpRequest):
    return render(request, "shop/main.html", {"items": Item.objects.all()})


def basket(request: HttpRequest):
    csrftoken = request.COOKIES.get("csrftoken")
    items: List[Item] = []
    currencies = {}

    if (basket_filter := Basket.objects.filter(customer_session=csrftoken)).exists():
        items = basket_filter.first().items.all()

    for item in items:
        if item.currency.code in currencies.keys():
            currencies[item.currency.code].append(item)
        else:
            currencies[item.currency.code] = [item]
    return render(request, "shop/basket.html", {"currencies": currencies})


def orders(request: HttpRequest):
    csrftoken = request.COOKIES.get("csrftoken")
    items: List[Item] = []

    if (orders_filter := Order.objects.filter(customer_session=csrftoken, paid=True)).exists():
        for order in orders_filter.all():
            items.extend(order.items.all())

    return render(request, "shop/orders.html", {"items": items})


def item(request: HttpRequest, id: int):
    print(request.user)
    csrftoken = request.COOKIES.get("csrftoken")
    in_basket = False

    if (basket_filter := Basket.objects.filter(customer_session=csrftoken)).exists():
        if basket_filter.first().items.filter(id=id).exists():
            in_basket = True

    return render(request, "shop/item.html", {"item": Item.objects.get(id=id), "in_basket": in_basket})


def success(request: HttpRequest, id: str):
    order = Order.objects.get(id=id)
    order.paid = True
    order.save()
    return render(request, "shop/success.html")


def error(request: HttpRequest):
    return render(request, "shop/error.html")


def pay_for_item(request: HttpRequest, id: int):
    csrftoken = request.COOKIES.get("csrftoken")

    order = Order(id=uuid.uuid4().hex + uuid.uuid4().hex,
                  customer_session=csrftoken)
    order.save()
    order.items.add(Item.objects.get(id=id))
    order.save()
    cancel_url = request.META["HTTP_REFERER"]
    success_url = f"http://{request.META['HTTP_HOST']}/success/{order.id}"
    stripe_checkout_session = get_stripe_checkout_session(order.items.all(),
                                                          success_url=success_url,
                                                          cancel_url=cancel_url)
    return redirect(stripe_checkout_session)


def pay_for_basket(request: HttpRequest, currency: str):
    csrftoken = request.COOKIES.get("csrftoken")

    if not (basket_filter := Basket.objects.filter(customer_session=csrftoken)).exists():
        return redirect("error")

    basket = basket_filter.first()
    currency = Currency.objects.get(code=currency)

    if currency is None:
        return redirect("error")

    if not (items_filter := basket.items.filter(currency=currency)).exists():
        return redirect("error")

    items = items_filter.all()
    order = Order(id=uuid.uuid4().hex + uuid.uuid4().hex,
                  customer_session=csrftoken)
    order.save()
    for item in items:
        order.items.add(item)
        basket.items.remove(item)
    order.save()
    basket.save()
    items_filter.delete()

    success_url = f"http://{request.META['HTTP_HOST']}/success/{order.id}".strip()
    cancel_url = request.META["HTTP_REFERER"]

    stripe_checkout_session = get_stripe_checkout_session(items,
                                                          success_url=success_url,
                                                          cancel_url=cancel_url)
    return redirect(stripe_checkout_session)
