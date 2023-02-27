from flask import Blueprint, render_template, redirect, request
from flask_security import roles_accepted, auth_required, logout_user
from model import db, Customer

staffBluePrint = Blueprint('staffpages', __name__)

class MyValidationError(Exception):
    pass

@staffBluePrint.route("/staffpage")
@auth_required()
@roles_accepted("Admin", "Staff")
def staffpage():
    q = request.args.get('q', '')
    errorCustomer = [' Customer do not exist! ']
    customers = Customer.query
    customers = customers.filter(
        Customer.Id.like( q ) |
        Customer.NationalId.like( q ))
    #if customers
     #  raise MyValidationError("Customer do not exist!")
    return render_template("staffpage.html",  q=q, customers = customers)


@staffBluePrint.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@staffBluePrint.route ("/contact")
@auth_required()
@roles_accepted("Admin", "Staff")
def contactpage():
    return render_template("contact.html")