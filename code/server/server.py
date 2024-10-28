#! /usr/bin/env python3.9

"""
server.py
Associate Developer Challenge
Python 3.9 or newer required.
"""

import json
import os
from flask_cors import cross_origin
import stripe
import re
import datetime
import calendar
import logging
from dataclasses import asdict
from itertools import groupby
from models.seller import Seller
from service.provision import provision
from service.provision import find_price, find_product

from flask import Flask, render_template, request
from dotenv import load_dotenv, find_dotenv
from flask_caching import Cache

if not os.path.exists("./.env"):
    logging.error("Please make sure valid .env file exist in code/server directory.")


load_dotenv(find_dotenv())

static_dir = str(os.path.abspath(os.path.join(__file__, "..", os.getenv("STATIC_DIR"))))

frontend = ""
if os.path.isfile("/".join([static_dir, "index.html"])):
    frontend = "vanilla"
else:
    frontend = "react"
    static_dir = str(os.path.abspath(os.path.join(__file__, "..", "./templates")))

server_dir = str(os.path.abspath(os.path.join(__file__, "../..")))

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

config = {
    "CACHE_TYPE": "SimpleCache",  # caching type
    "CACHE_DEFAULT_TIMEOUT": 300,  # default Cache Timeout
}

app = Flask(
    __name__, static_folder=static_dir, static_url_path="", template_folder=static_dir
)

# Flask to use the above defined config
app.config.from_mapping(config)

cache = Cache(app)
cache.init_app(app)


@app.route("/", methods=["GET"])
def get_main_page():
    """Display langing page"""
    # Display landing page
    if frontend == "vanilla":
        return render_template("index.html")
    else:
        return render_template("react_redirect.html")


@app.route("/signup", methods=["GET"])
def get_signup_page():
    """Display the signup page"""
    # Display signup page
    if frontend == "vanilla":
        return render_template("signup.html")
    else:
        return render_template("react_redirect.html")


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard_page():
    """Display the leaderboard page"""
    # Display leaderboard page
    if frontend == "vanilla":
        return render_template("leaderboard.html")
    else:
        return render_template("react_redirect.html")


@cache.cached(timeout=6000, key_prefix="price")
def get_price_id_from_cache():
    """Get the Price Id of the Product

    Returns:
        string: Price Id from the Cache
    """
    challenge_id = os.getenv("CHALLENGE_ID")
    product = cache.get("product")
    if product is None:
        product = find_product(challenge_id)

    price = find_price(product_id=product.id, lookup_key=[challenge_id])
    # TODO: Integrate Stripe
    return price.id


def validate_email(input_email):
    """Validate the Email Address is valid String format. Use this function to ensure that only one payment link is created per email.

    Args:
        input_email (string): Input Email Address

    Returns:
        boolean: True, if valid Email Format
    """
    mail_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(mail_regex, input_email):
        return True
    else:
        return False


# TODO: Integrate Stripe


@app.route("/create-payment-link", methods=["POST"])
@cross_origin()
def create_payment_link():
    """Create Stripe Payment Link
    Note:
    Milestone 1: Creating Payment Links
    Validate the Email Address is valid String format.
    After email address validation, create a new Payment Link for the fan, if one does not exists.

    Returns:
        object: Stripe Payment Link
    """
    try:
        data = request.get_json()
        email = data['email']
        display_name = data['display_name']
        if not validate_email(email):
            raise Exception('Email address is not valid')
        price_id = get_price_id_from_cache()
        metadata={ "fan_email": email, "fan_name": display_name }

        response = stripe.PaymentLink.list()
        payment_link = next((item.url for item in response.data if item.metadata == metadata and item.active), None)

        if payment_link is None:
            payment_link = stripe.PaymentLink.create(
                line_items=[{ "price": price_id, "quantity": 1 }],
                metadata=metadata
            ).url

        # TODO: Integrate Stripe
        # returns config information that is used by the client JavaScript to display the page.

        return {
            "paymentLink": payment_link,
        }
    except Exception as e:
        return {"error": str(e)}, 403


@app.route("/leaders", methods=["GET"])
@cross_origin()
def get_leaders():
    """Get the Leaderboard data leveraging manual pagination of the Checkout sessions to total amount by fan email address
    Note:
    Milestone 2: Leaderboard
    Returns:
        Json Array: seller array with name, email, and total amount that is sorted desc by total amount
    """
    try:
        sessions = stripe.checkout.Session.list(limit=500)
        sellers = [
            Seller(
                name=session.metadata.fan_name, 
                email=session.metadata.fan_email, 
                amount=sum(
                    [item.amount_total if item.metadata.fan_email == session.metadata.fan_email else 0 for item in sessions.data if hasattr(item.metadata, 'fan_email') and hasattr(item.metadata, 'fan_name')]
                )
            )
            for session in sessions.data if hasattr(session.metadata, 'fan_email') and hasattr(session.metadata, 'fan_name')
        ]
        sellers = [seller for index, seller in enumerate(sellers) if sellers.index(seller) == index]
        sellers.sort(reverse=True, key=lambda seller: seller.amount)

        # TODO: Integrate Stripe
        # returns config information that is used by the client JavaScript to display the page.
        return {
            "sellers": sellers,
        }

    except Exception as e:
        err_msg = 'Error in GET /leaders: Threw {} with args {}'.format(type(e).__name__, e.args)
        print(err_msg)
        return {"error": err_msg}, 500


# TODO: Integrate Stripe

provision(cache)

if __name__ == "__main__":
    app.run()
