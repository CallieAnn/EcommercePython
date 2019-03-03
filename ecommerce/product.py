import os;
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import stripe;

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


bp = Blueprint('product', __name__)


@bp.route('/')
def index():

    return render_template('product/home.html')


@bp.route('/createproduct', methods=('GET', 'POST'))
def createproduct():
    if request.method == 'POST':
        pName = request.form['name']
        pPrice = request.form['price']
        pQuantity = request.form['quantity']
        pLocations = request.form['locations']
        pDescription = request.form['description']

        error = ""

        if not pName:
            error = 'Name is required.'
        if not pPrice:
            error += '\nPrice is required.'
        if not pQuantity:
            error += '\nQuantity is required.'
        if not pLocations:
            error += '\nLocation is required.'
        if error == "":
            # do something with product later, return to products page
            stripe.Product.create(
                name=pName,
                type='good',
                description=pDescription,
                metadata={'locations': pLocations, 'Quantity': pQuantity, 'Price': pPrice}
            )

            return redirect(url_for('products.html'))

        flash(error)

    return render_template('product/createproduct.html')


@bp.route('/products')
def products():
    storedProducts = stripe.Product.list(limit=10)

    return render_template('product/products.html', products=storedProducts)


@bp.route('/about')
def about():
    return render_template('product/about.html')


@bp.route('/checkout')
def checkout():
    return render_template('product/checkout.html', key=stripe_keys['publishable_key'])


@bp.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 10000

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('product/charge.html', amount=amount)