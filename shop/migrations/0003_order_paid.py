# Generated by Django 4.1.1 on 2022-09-14 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_rename_product_item_rename_products_order_items"),
    ]

    operations = [
        migrations.AddField(
            model_name="order", name="paid", field=models.BooleanField(default=False),
        ),
    ]
