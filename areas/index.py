from flask import Blueprint, render_template
from model import  Customer, Account

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
    # account = Account.query.filter(Account.Balance)
    # sweden = Customer.query.filter_by(Customer.TelephoneCountryCode=="46"()) 
    # allAccounts = Account.query.count()
    # customers = Customer.query.count()
    # totalBalance  =  0
    # for x in sweden:
    #     totalBalance += x.Balance
    # # for x in account:
    # #     totalBalance += x.Balance 
    return render_template("country/sweden.html")


@indexBluePrint.route("/norway")
def StatisticNorway():
        # account = Account.query.filter(Account.Balance)
    # sweden = Customer.query.filter_by(Customer.TelephoneCountryCode=="47"()) 
    # allAccounts = Account.query.count()
    # customers = Customer.query.count()
    # totalBalance  =  0
    # for x in sweden:
    #     totalBalance += x.Balance
    # # for x in account:
    # #     totalBalance += x.Balance 
    return render_template("country/norway.html" )

@indexBluePrint.route("/us")
def StatisticUs():
    return render_template("country/us.html" )