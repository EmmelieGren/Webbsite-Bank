from flask import Blueprint, render_template, redirect
from flask_security import roles_accepted, auth_required, logout_user
from model import db, Customer, Account, Transaction
from forms import TransactionForm, TransferForm
from datetime import datetime

today = datetime.now()

transactionBluePrint = Blueprint('transactionpage', __name__)

@transactionBluePrint.route("/customer/account/withdraw/<id>", methods=['GET', 'POST'])
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


@transactionBluePrint.route("/customer/account/deposit/<id>", methods=['GET', 'POST'])
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


@transactionBluePrint.route("/customer/account/transfer/<id>", methods=['GET', 'POST'])
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