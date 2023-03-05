from flask import Blueprint, render_template, redirect
from flask_security import roles_accepted, auth_required
from model import db, Account, Transaction
from forms import TransactionForm, TransferForm
from .services import getTransactions, getAccounts, getCustomers, getDate

transactionBluePrint = Blueprint('transactionpage', __name__)

@transactionBluePrint.route("/customer/account/withdraw/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin","Staff")
def Withdraw(id):
    form =TransactionForm()                               
    account = getAccounts(id)
    customer = getCustomers(id)
    transaction =  getTransactions(id)
    large = ['Amount is larger then your balance!']
 
    if form.validate_on_submit():
        if account.Balance < form.Amount.data:
                form.Amount.errors = form.Amount.errors + large
        else:
            account = getAccounts(id)
            transaction = getTransactions(id)
            customer =  getCustomers(id)
            account.Balance = account.Balance - form.Amount.data
            newWithdraw = Transaction()
            newWithdraw.Type = transaction.Type
            newWithdraw.Operation = "Personal Withdraw"
            newWithdraw.Date = getDate()
            newWithdraw.Amount = form.Amount.data
            newWithdraw.NewBalance = account.Balance - form.Amount.data
            newWithdraw.AccountId = account.Id
            db.session.add(newWithdraw)
            db.session.commit()
            return redirect("/customer/" + str(account.CustomerId))

    return render_template("transactions/withdraw.html", account = account, customer = customer, formen=form, transaction = transaction)


@transactionBluePrint.route("/customer/account/deposit/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin","Staff")
def Deposit(id):
    form =TransactionForm()                               
    account = getAccounts(id)
    customer = getCustomers(id)
    transaction = getTransactions(id)

    if form.validate_on_submit():
        account.Balance = account.Balance + form.Amount.data
        newDeposit = Transaction()
        newDeposit.Type = transaction.Type
        newDeposit.Operation = "Personal Deposit"
        newDeposit.Date = getDate()
        newDeposit.Amount = form.Amount.data
        newDeposit.NewBalance = account.Balance + form.Amount.data
        newDeposit.AccountId = account.Id
        db.session.add(newDeposit)
        db.session.commit()
        return redirect("/customer/" + str(account.CustomerId))

    return render_template("transactions/deposit.html", account=account, customer = customer, formen=form, transaction = transaction)


@transactionBluePrint.route("/customer/account/transfer/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin","Staff")
def Transfer(id):
    form =TransferForm()
    account = getAccounts(id)
    receiver = Account.query.filter_by(Id = form.Id.data).first()
    transactionSender = Transaction() 
    transactionReceiver = Transaction()
    errorAmount = ['Amount is larger then your balance!']
    errorAccountDoNotExist = [' Account do not exist! ']
    errorSameAccount = [' Cant transfer to same account! ']


    if form.validate_on_submit():
        if account.Balance < form.Amount.data:
            form.Amount.errors = form.Amount.errors + errorAmount
        elif receiver == None:
            form.Id.errors = form.Id.errors + errorAccountDoNotExist
        elif receiver.Id == account.Id:
            form.Id.errors = form.Id.errors + errorSameAccount

        else:
            transactionSender.Amount = form.Amount.data
            account.Balance = account.Balance - transactionSender.Amount
            transactionSender.NewBalance = account.Balance
            transactionSender.AccountId = account.Id
            transactionSender.Date = getDate()
            transactionSender.Type = "Credit"
            transactionSender.Operation = "Transfer"

            transactionReceiver.Amount= form.Amount.data
            receiver.Balance = receiver.Balance + transactionReceiver.Amount
            transactionReceiver.NewBalance = receiver.Balance
            transactionReceiver.AccountId = receiver.Id
            transactionReceiver.Date = getDate()
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