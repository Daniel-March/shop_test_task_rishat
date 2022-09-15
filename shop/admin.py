from django.contrib import admin

from shop.models import Currency, Item, Order, Basket

admin.site.register(Currency)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Basket)
