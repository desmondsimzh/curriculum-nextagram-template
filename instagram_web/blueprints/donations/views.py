import os
from braintree import BraintreeGateway, Configuration, Environment
from flask import Blueprint, render_template, redirect, request, url_for, flash, Flask
from models.image import Image
from models.user import User
from models.donate import Donate
from flask_login import login_required, current_user


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

gateway = BraintreeGateway(Configuration(
        Environment.Sandbox,
        merchant_id=os.getenv("BT_MERCHANT_ID"),
        public_key=os.getenv("BT_PUBLIC_KEY"),
        private_key=os.getenv("BT_PRIVATE_KEY")
    ))

@donations_blueprint.route("/<id>/new")
@login_required
def new(id):
    token = gateway.client_token.generate()
    return render_template("donations/new.html", token=token, image_id=id)

@donations_blueprint.route("/<id>/pay", methods=["POST"])
@login_required
def pay(id):
    donation = Donate.create(user_id = current_user.id, image_id = id , donate_amount =request.form.get('donate_amount'))
    donation.save()
    result= gateway.transaction.sale({
        "amount": request.form.get('donate_amount'),
        "payment_method_nonce": request.form['nonce'],
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        flash("Thank you for your donation!", "success")
        return redirect(url_for('users.show' , username = current_user.name))
    else:
        flash("Payment failure, please try agian.")
        return redirect(url_for('donations.new', id=id))



