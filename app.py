from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, Customer, Account, Transaction
from flask_security import roles_accepted, auth_required, logout_user
from random import randint
import os 
from datetime import datetime


from areas.customerpage import customerBluePrint
from areas.transactionpage import transactionBluePrint
from areas.adminpages import adminBluePrint


today = datetime.now()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/bank'
#app.config['SECRET_KEY'] = os.urandom(32)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"

db.app = app
db.init_app(app)
migrate = Migrate(app,db)


app.register_blueprint(customerBluePrint)
app.register_blueprint(transactionBluePrint)
app.register_blueprint(adminBluePrint)


@app.route("/")
def startpage():
    account = Account.query.filter(Account.Balance)
    totalBalance  =  0
    allAccounts = Account.query.count()
    customers = Customer.query.count()
    for x in account:
        totalBalance += x.Balance 
    return render_template("index.html", allAccounts= allAccounts, customers = customers, totalBalance=totalBalance )


@app.route("/sweden")
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

    

@app.route("/norway")
def StatisticNorway():
    return render_template("country/norway.html" )

@app.route("/us")
def StatisticUs():
    return render_template("country/us.html" )

if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData(app,db)
        app.run(debug = True)