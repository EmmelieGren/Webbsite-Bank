from flask import Blueprint, render_template
from model import db, Customer, Account

indexBluePrint = Blueprint('index', __name__)


@indexBluePrint.route("/admin")

@indexBluePrint.route("/")
def startpage():
    account = Account.query.filter(Account.Balance)
    totalBalance  =  0
    allAccounts = Account.query.count()
    customers = Customer.query.count()
    for x in account:
        totalBalance += x.Balance 
    return render_template("index.html", allAccounts= allAccounts, customers = customers, totalBalance=totalBalance )

@indexBluePrint.route("/sweden")
def StatisticSweden():
    account = Account.query.filter(Account.Balance)
    customer = Customer.query.filter(Customer.CountryCode)
    totalBalance  =  0
    allAccounts = Account.query.count()
    customers = Customer.query.count()
    sweden = 0
    for se in customer:
        sweden += se.CountryCode("SE")
    for x in account:
        totalBalance += x.Balance 
    return render_template("country/sweden.html", allAccounts= allAccounts, customers = customers, totalBalance=totalBalance, sweden = sweden )


@indexBluePrint.route("/norway")
def StatisticNorway():
    return render_template("country/norway.html" )

@indexBluePrint.route("/us")
def StatisticUs():
    return render_template("country/us.html" )