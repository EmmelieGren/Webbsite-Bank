from flask import Blueprint, render_template, redirect, request
from flask_security import roles_accepted, auth_required, logout_user
from model import db, Customer

adminBluePrint = Blueprint('adminpages', __name__)

@adminBluePrint.route("/admin")
@auth_required()
@roles_accepted("Admin")
def adminpage():
    q = request.args.get('q', '')
    errorCustomer = [' Customer do not exist! ']
    customers = Customer.query
    customers = customers.filter(
        Customer.Id.like( q ) |
        Customer.NationalId.like( q ))
    if q == customers:
        return render_template("admin.html",  q=q, customers = customers)
    else:
        # raise ValueError ("wrong cust")
        return render_template("admin.html",  q=q, customers = customers)


@adminBluePrint.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@adminBluePrint.route ("/contact")
def contactpage():
    return render_template("contact.html")