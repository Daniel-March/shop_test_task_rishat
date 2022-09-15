from typing import List
import os

import stripe
from dotenv import load_dotenv

from shop.models import Item

load_dotenv()

stripe_api_key = os.getenv("STRIPE_API_KEY")

stripe.api_key = stripe_api_key


def get_stripe_checkout_session(items: List[Item], success_url: str, cancel_url: str):
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": item.currency.code,
                    "product_data": {
                        "name": item.name
                    },
                    "unit_amount": item.price * item.currency.coefficient
                },
                "quantity": 1,
            } for item in items
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return checkout_session.url
