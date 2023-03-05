
from app import app
from model import db, Transaction, Account
from areas.services import getDate


def test_deposit():

    newaccount = Account()
    newaccount.Id = 1
    newaccount.Balance = 500
    deposit = Transaction()
    deposit.Amount = 10
    create_deposit(newaccount, deposit, "Salary")

    assert newaccount.Balance == 510
    assert deposit.NewBalance == 510
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
    newaccount.Id = 132
    newaccount.Balance = 500
    withdraw = Transaction()
    withdraw.Amount = 400
    create_withdraw(newaccount, withdraw, "Payment")

    assert newaccount.Balance == 100
    assert withdraw.NewBalance == 100
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




def test_transfer():

    sender = Account()
    sender.Id = 1
    sender.Balance = 20

    receiver = Account()
    receiver.Id = 2
    receiver.Balance = 10

    transferSender = Transaction()
    transferSender.Amount = 10
    transferReceiver = Transaction()
    transferReceiver.Amount = 10
 
    create_transaction(sender, receiver, transferSender, transferReceiver, "Transfer")

    assert sender.Balance == 10
    assert transferSender.NewBalance == 10
    assert receiver.Balance == 20
    assert transferReceiver.NewBalance == 20

    assert sender.Id == transferSender.AccountId
    assert receiver.Id == transferReceiver.AccountId
    assert transferSender.AccountId == sender.Id
    assert transferReceiver.AccountId == receiver.Id

    assert transferSender.Date != None
    assert transferReceiver.Date != None
    assert transferSender.Type == "Debit"
    assert transferReceiver.Type == "Debit"
    assert transferSender.Operation == "Transfer"
    assert transferReceiver.Operation == "Transfer"

    assert transferSender in sender.Transactions
    assert transferReceiver in receiver.Transactions

def create_transaction(sender, receiver, send, receive, operation):
    now = getDate()

    sender.Balance = sender.Balance - send.Amount
    send.NewBalance = sender.Balance
    send.AccountId = sender.Id
    send.Date = now
    send.Type = "Debit"
    send.Operation = operation
    sender.Transactions.append(send)

    receiver.Balance = receiver.Balance + receive.Amount
    receive.NewBalance = receiver.Balance
    receive.AccountId = receiver.Id
    receive.Date = now
    receive.Type = "Debit"
    receive.Operation = operation
    receiver.Transactions.append(receive)