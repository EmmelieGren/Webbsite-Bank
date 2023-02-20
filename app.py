from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, Customer, Account, Transaction
from flask_security import roles_accepted, auth_required, logout_user
from random import randint
from forms import NewCustomerForm, NewAccountForm, TransactionForm, TransferForm
import os 
from datetime import datetime


from areas.customerpage import customerBluePrint


today = datetime.now()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/bank'
# app.config['SECRET_KEY'] = os.urandom(32)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"

db.app = app
db.init_app(app)
migrate = Migrate(app,db)


app.register_blueprint(customerBluePrint)


@app.route("/")
def startpage():
    account = Account.query.filter(Account.Balance)
    totalBalance  =  0
    allAccounts = Account.query.count()
    customers = Customer.query.count()
    for x in account:
        totalBalance += x.Balance 
    return render_template("index.html", allAccounts= allAccounts, customers = customers, totalBalance=totalBalance )

@app.route("/contact")
def contactpage():
    return render_template("contact.html")

@app.route("/admin")
@auth_required()
@roles_accepted("Admin")
def adminpage():
    q = request.args.get('q', '')
    customers = Customer.query
    customers = customers.filter(
        Customer.Id.like( q ) |
        Customer.NationalId.like( q ))
    if q == Customer.Id:
        return render_template("admin.html",  q=q, customers = customers)
    else:
        pass
        return render_template("admin.html",  q=q, customers = customers)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/customer/account/withdraw/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
def Withdraw(id):
    form =TransactionForm()                               
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    transaction = Transaction.query.filter_by(Id = id).first()

    # if form.Amount.data < account.Balance:
    #     raise Exception("To hig withdraw")  

    if form.validate_on_submit():
        account = Account.query.filter_by(Id = id).first()
        transaction = Transaction.query.filter_by(Id = id).first()
        customer = Customer.query.filter_by(Id = id).first()
        account.Balance = account.Balance - form.Amount.data
        newWithdraw = Transaction()
        newWithdraw.Type = transaction.Type
        newWithdraw.Operation = "Personal Withdraw"
        newWithdraw.Date = today
        newWithdraw.Amount = form.Amount.data
        newWithdraw.NewBalance = account.Balance - form.Amount.data
        newWithdraw.AccountId = account.Id
        db.session.add(newWithdraw)
        db.session.commit()
        return redirect("/customer/" + str(account.CustomerId))
    return render_template("transactions/withdraw.html", account = account, customer = customer, formen=form, transaction = transaction)

@app.route("/customer/account/deposit/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
def Deposit(id):
    form =TransactionForm()                               
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    transaction = Transaction.query.filter_by(Id = id).first()

    if form.validate_on_submit():
        account.Balance = account.Balance + form.Amount.data
        newDeposit = Transaction()
        newDeposit.Type = transaction.Type
        newDeposit.Operation = "Personal Deposit"
        newDeposit.Date = today
        newDeposit.Amount = form.Amount.data
        newDeposit.NewBalance = account.Balance + form.Amount.data
        newDeposit.AccountId = account.Id
        db.session.add(newDeposit)
        db.session.commit()
        return redirect("/customer/" + str(account.CustomerId))
    return render_template("transactions/deposit.html", account=account, customer = customer, formen=form, transaction = transaction)

@app.route("/customer/account/transfer/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
def Transfer(id):
    form =TransferForm()
    account = Account.query.filter_by(Id = id).first()
    receiver = Account.query.filter_by(Id = form.Id.data).first()
    transactionSender = Transaction() 
    transactionReceiver = Transaction()

    if form.validate_on_submit():

        transactionSender.Amount = form.Amount.data
        account.Balance = account.Balance - transactionSender.Amount
        transactionSender.NewBalance = account.Balance
        transactionSender.AccountId = account.Id
        transactionSender.Date = today
        transactionSender.Type = "Credit"
        transactionSender.Operation = "Transfer"

        transactionReceiver.Amount= form.Amount.data
        receiver.Balance = receiver.Balance + transactionReceiver.Amount
        transactionReceiver.NewBalance = receiver.Balance
        transactionReceiver.AccountId = receiver.Id
        transactionReceiver.Date = today
        transactionReceiver.Type = "Debit"
        transactionReceiver.Operation = "Transfer"

        db.session.add(account)
        db.session.add(receiver)
        db.session.add(transactionReceiver)
        db.session.add(transactionSender)
        db.session.commit()
        
        return redirect("/customer/" + str(account.CustomerId))
    return render_template("transactions/transfer.html",  
                                            formen=form,
                                            account = account, 
                                            receiver=receiver, 
                                            transactionReceiver=transactionReceiver, 
                                            transactionSender=transactionSender,
                                            )


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