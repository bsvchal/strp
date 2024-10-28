import json
import os
import stripe
from dataclasses import asdict
from models.product import Product
from models.price import Price

T_SHIRT_PRODUCT_NAME = "The Afrobeatles T-Shirt"
T_SHIRT_PRODUCT_DESC = "Afrobeatles Tour"
T_SHIRT_LOOKUP_KEY = os.getenv("CHALLENGE_ID")
T_SHIRT_URL = os.getenv("CHALLENGE_ID")
T_SHIRT_COST = 2500


def find_product(url):
    """find_product Find existing Product
    Milestone 1
    Args:
        url (string): Unique Url

    Returns:
        product: Product
    """
    try:
        result = stripe.Product.list(url=url, limit=1)
        item = result.data.pop()
        product = Product(
            id=item.id, 
            name=item.name, 
            price=None
        )
    except Exception as e:
        print(f"find_product() -> { e }")
        return None    
    # TODO: set stripe_product to an instance of the product model, i.e.
    # stripe_product = Product(<product id>,<name>, <price>)
    
    return product


def find_price(product_id, lookup_key):
    """find_price Finds an existing Price with Stripe for the product.
    Milestone 1
    Args:
        product_id (string): Stripe Product Id
        lookup_key (string): Lookup Key

    Returns:
        price: a Price object
    """
    try:
        result = stripe.Price.list(product=product_id, lookup_keys=lookup_key, limit=1)
        item = result.data.pop()
        price = Price(
            id=item.id,
            nickname=item.nickname,
            currency=item.currency,
            unit_amount=item.unit_amount,
            lookup_key=item.lookup_key
        )
    except Exception as e:
        print(f"find_price() -> { e }")
        return None
    # TODO: Returns an instance of the local Price model
    # result = Price(<id>, <nickname>, <currency>, <amount>, <lookup_key>)

    return price


def create_price(product, unit_amount, nickname, lookup_keys):
    """create_price Create Price
    Milestone 1
    We may want to adjust the details of this price over time, without having to change how we refer to it, so use the transfer_lookup_key parameter.
    Args:
        product (string): Product Id
        unit_amount (int): Unit Amount
        nickname (string): Nickname
        lookup_keys (string): lookup_key

    Returns:
        price: Price
    """
    result = stripe.Price.create(
        product=product,
        currency="usd",
        unit_amount=unit_amount,
        nickname=nickname,
        lookup_key=lookup_keys,
        transfer_lookup_key=True
    )
    price = Price(
        id=result.id, 
        nickname=result.nickname, 
        currency=result.currency, 
        unit_amount=result.unit_amount, 
        lookup_key=result.lookup_key
    )
    # TODO: Return Price
    # Returns an instance of the local Price model
    # result = Price(<id>, <nickname>, <currency>, <amount>, <lookup_key>)
    return price


def create_product(name, description, url):
    """create_product Create a Product with in Stripe
    Milestone 1
    Args:
        name (string): Name
        description (string): Description
        url (string): Url

    Returns:
        product: a Stripe Product
    """
    result = stripe.Product.create(name=name, description=description, url=url)
    product = Product(id=result.id, name=result.name, price=None)
    # TODO: Return the Product created in Stripe
    return product


def provision(cache):
    """Create the Product and Price for challenge.
    Leverage Challenge ID as unique URL for the product.
    Leverage Challenge ID as unique lookup key for the price.
    Milestone 1
    """
    try:
        # Clear in-memory cache
        cache.clear()

        # Check if Product exists with correct shape in Stripe Account
        stripe_product = find_product(T_SHIRT_URL)
        price = None
        if stripe_product is not None:
            # Check for Prices
            price = find_price(stripe_product.id, [T_SHIRT_LOOKUP_KEY])

            # Throw error if either Price doesn't exist
            if price is None:
                price = create_price(
                    stripe_product.id,
                    T_SHIRT_COST,
                    T_SHIRT_PRODUCT_NAME,
                    T_SHIRT_LOOKUP_KEY,
                )
        else:
            # Product does not exist in Stripe, create it and its Prices
            stripe_product = create_product(
                T_SHIRT_PRODUCT_NAME, T_SHIRT_PRODUCT_DESC, T_SHIRT_URL
            )
            if stripe_product is not None:
                price = create_price(
                    stripe_product.id,
                    T_SHIRT_COST,
                    T_SHIRT_PRODUCT_NAME,
                    T_SHIRT_LOOKUP_KEY,
                )

        if stripe_product is not None:
            stripe_product.price = asdict(price)

        if price is None or stripe_product is None:
            print("TODO: Implement provisioning service to create a Product & Price")
        else:
            cache.set("product", stripe_product, timeout=10 * 60)
    except Exception:
        print("Error during provisioning")
        raise
