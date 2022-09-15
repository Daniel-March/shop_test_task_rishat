from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=120, null=False)
    code = models.CharField(max_length=3, null=False)
    coefficient = models.IntegerField(default=100, null=False)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=120, null=False)
    description = models.TextField(null=False)
    price = models.IntegerField(null=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Basket(models.Model):
    customer_session = models.CharField(max_length=32)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.customer_session


class Order(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    customer_session = models.CharField(max_length=32)
    items = models.ManyToManyField(Item)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_session
