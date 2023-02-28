from flask import Blueprint, render_template, redirect, request, flash
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
    customers = Customer.query
    customers = customers.filter(
        Customer.Id.like( q ) |
        Customer.NationalId.like( q ))
    if customers == None:
        error = 'Invalid credentials'
        # flash ('Customer does not exisit')
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