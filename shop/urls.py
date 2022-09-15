from django.urls import path

from shop import views as shop_views
from shop import actions as shop_actions

urlpatterns = [
    path('', shop_views.main, name="main"),
    path('basket', shop_views.basket, name="basket"),
    path('orders', shop_views.orders, name="orders"),
    path('success/<str:id>', shop_views.success, name="success"),
    path('error', shop_views.error, name="error"),
    path('item/<int:id>/buy', shop_views.pay_for_item, name="pay_for_item"),
    path('basket/buy/<str:currency>', shop_views.pay_for_basket, name="pay_for_basket"),
    path('item/<int:id>', shop_views.item, name="item"),

    path('basket/add/<int:id>', shop_actions.add_item_to_basket, name="add_item_to_basket"),
    path('basket/remove/<int:id>', shop_actions.remove_item_from_basket, name="remove_item_from_basket"),
]
