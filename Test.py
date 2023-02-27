
from app import app
from model import db, Transaction, Customer, Account
from areas.services import getDate
import pytest


def test_deposit():

    newaccount = Account()
    newaccount.Id = 1
    newaccount.Balance = 500
    deposit = Transaction()
    deposit.Amount = 10
    create_deposit(newaccount, deposit, "Salary")

    assert newaccount.Balance == 10
    assert deposit.NewBalance == 10
    assert newaccount.Id == deposit.AccountId
    assert deposit.Date != None
    assert deposit.Type == "Debit"
    assert deposit.Operation == "Salary"
    assert len(newaccount.Transactions) > 0
    assert deposit in newaccount.Transactions

def create_deposit(account, deposit, operation):

    account.Balance = account.Balance + deposit.Amount
    deposit.NewBalance = account.Balance
    deposit.AccountId = account.Id
    deposit.Date = getDate()
    deposit.Type = "Debit"
    deposit.Operation = operation
    account.Transactions.append(deposit)



def test_withdraw():

    newaccount = Account()
    newaccount.Id = 1
    newaccount.Balance = 500
    withdraw = Transaction()
    withdraw.Amount = 600
    create_deposit(newaccount, withdraw, "Payment")

    assert newaccount.Balance == 10
    assert withdraw.NewBalance == 10
    assert newaccount.Id == withdraw.AccountId
    assert withdraw.Date != None
    assert withdraw.Type == "Credit"
    assert withdraw.Operation == "Payment"
    assert len(newaccount.Transactions) > 0
    assert withdraw in newaccount.Transactions

def create_withdraw(account, withdraw, operation):

    account.Balance = account.Balance - withdraw.Amount
    withdraw.NewBalance = account.Balance
    withdraw.AccountId = account.Id
    withdraw.Date = getDate()
    withdraw.Type = "Credit"
    withdraw.Operation = operation
    account.Transactions.append(withdraw)
