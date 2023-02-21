from model import Customer, Account, Transaction
from datetime import datetime

def getCustomers(id):
    return Customer.query.filter_by(Id = id).first()

def getAccounts(id):
    return Account.query.filter_by(Id = id).first()

def getTransactions(id):
    return Transaction.query.filter_by(Id = id).first()

def getDate():
    return  datetime.now()

