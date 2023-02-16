from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, Customer, Account, Transaction
from flask_security import roles_accepted, auth_required, logout_user
# from random import randint
from forms import NewCustomerForm, NewAccountForm, TransactionForm
import os 
from datetime import date, datetime

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
    return render_template("contact.html",activePage="contactPage")

@app.route("/admin")
@auth_required()
@roles_accepted("Admin")
def adminpage():
    return render_template("admin.html", activePage="secretPage")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/customer/<id>")
# @auth_required()
# @roles_accepted("Admin","Staff")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    summa  =  0
    for accounts in customer.Accounts:
        summa = summa + accounts.Balance
    return render_template("customer.html", customer=customer,  summa=summa )

@app.route("/customer/account/<id>")
def Transaktioner(id):
    account = Account.query.filter_by(Id = id).first()
    transaktioner = Transaction.query.filter_by(AccountId=id)
    transaktioner = transaktioner.order_by(Transaction.Date.desc())
    return render_template("transactions.html", account=account, transaktioner=transaktioner)

@app.route("/newaccount/<id>", methods=['GET', 'POST'])
def newaccount(id):
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    form = NewAccountForm()
    if form.validate_on_submit():
        newaccount =  Account()
        newaccount.Id = customer
        newaccount.AccountType = form.AccountType.data
        newaccount.Created = today
        newaccount.Balance = 0
        #customer.Accounts = customer.Accounts + newaccount
        db.session.add(newaccount)
        db.session.commit()
        return redirect("/customer/account/<id>" )
    return render_template("newaccount.html", formen=form, customer = customer, account = account )




@app.route("/customer/account/withdraw/<id>", methods=['GET', 'POST'])
def Withdraw(id):
    form =TransactionForm()                               
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    transaction = Transaction.query.filter_by(Id = id).first()

    # if form.Amount.data < account.Balance:
    #     raise Exception("To hig withdraw")  

    if form.validate_on_submit():
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
        return redirect("/customer/account/<id>")

    return render_template("withdraw.html", account = account, customer = customer, formen=form, transaction = transaction)

@app.route("/customer/account/deposit/<id>", methods=['GET', 'POST'])
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

        return redirect("/customer/account/<id>")
    return render_template("deposit.html", account=account, customer = customer, formen=form, transaction = transaction)





@app.route("/customer/transfer", methods=['GET', 'POST'])
def Transfer(id):
    form =TransactionForm()                               
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()

    # if form.validate_on_submit():
    #     newDeposit = Transaction()
    #     newDeposit.Type = "Personal Deposit"
    #     newDeposit.Date = form.Date.data
    #     newDeposit.Amount = form.Amount.data
    #     newDeposit.NewBalance = Account.Balance + form.Amount.data
    #     db.session.add(newDeposit)
    #     db.session.commit()

    #    return redirect("/customer/account/<id>")
    return render_template("transfer.html", account=account, customer = customer,formen=form)



@app.route("/customers")
# @auth_required()
# @roles_accepted("Admin","Staff")
def customersPage():
    sortColumn = request.args.get('sortColumn', 'name')
    sortOrder = request.args.get('sortOrder', 'asc')
    q = request.args.get('q', '')
    page = int(request.args.get('page', 1))

    customers = Customer.query

    customers = customers.filter(
        Customer.Surname.like('%' + q + '%') |
        Customer.GivenName.like('%' + q + '%') |
        Customer.Id.like('%' + q + '%') |
        Customer.NationalId.like('%' + q + '%') |
        Customer.City.like('%' + q + '%'))
        
    if sortColumn == "name":
        if sortOrder == "asc":
            customers = customers.order_by(Customer.Surname.asc())
        else:
            customers = customers.order_by(Customer.Surname.desc())
    elif sortColumn == "city":
        if sortOrder == "asc":
            customers = customers.order_by(Customer.City.asc())
        else:
            customers = customers.order_by(Customer.City.desc())

    paginationObject = customers.paginate(page=page, per_page=10, error_out=False)
    return render_template("customers.html",
                            customers=paginationObject.items,
                            pages=paginationObject.pages,
                            sortOrder=sortOrder,
                            sortColumn=sortColumn,
                            has_next=paginationObject.has_next,
                            has_prev=paginationObject.has_prev,
                            page=page,
                            q=q
                            )

@app.route("/newcustomer", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin")
def newcustomer():
    form = NewCustomerForm()
    if form.validate_on_submit():
        customer = Customer()
        customer.GivenName = form.givenName.data
        customer.Surname = form.surname.data
        customer.Streetaddress = form.streetaddress.data
        customer.City = form.city.data
        customer.Zipcode = form.zipcode.data
        customer.Country = form.country.data
        customer.CountryCode = form.countryCode.data
        customer.Birthday = form.birthday.data
        customer.NationalId = form.nationalId.data
        customer.TelephoneCountryCode = form.telephoneCountryCode.data
        customer.Telephone = form.telephone.data
        customer.EmailAddress = form.emailAddress.data
        newaccount = Account()
        newaccount.AccountType = "Checking"
        newaccount.Created = today
        newaccount.Balance = 0
        customer.Accounts = [newaccount]

        db.session.add(customer)
        db.session.commit()
        return redirect("/" )
    return render_template("newcustomer.html", formen=form )

@app.route("/editcustomer/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin")
def editcustomer(id):
    customer = Customer.query.filter_by(Id=id).first()
    form = NewCustomerForm()
    if form.validate_on_submit():
        customer.GivenName = form.givenName.data
        customer.Surname = form.surname.data
        customer.Streetaddress = form.streetaddress.data
        customer.City = form.city.data
        customer.Zipcode = form.zipcode.data
        customer.Country = form.country.data
        customer.CountryCode = form.countryCode.data
        customer.Birthday = form.birthday.data
        customer.NationalId = form.nationalId.data
        customer.TelephoneCountryCode = form.telephoneCountryCode.data
        customer.Telephone = form.telephone.data
        customer.EmailAddress = form.emailAddress.data
        db.session.commit()
        return redirect("/customers" )
    if request.method == 'GET':
        form.givenName.data = customer.GivenName
        form.surname.data = customer.Surname
        form.streetaddress.data = customer.Streetaddress
        form.city.data = customer.City
        form.zipcode.data = customer.Zipcode
        form.country.data = customer.Country
        form.countryCode.data = customer.CountryCode
        form.birthday.data = customer.Birthday
        form.nationalId.data = customer.NationalId
        form.telephoneCountryCode.data = customer.TelephoneCountryCode
        form.telephone.data = customer.Telephone
        form.emailAddress.data = customer.EmailAddress
    return render_template("editcustomer.html", formen=form )


if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData(app,db)
        app.run(debug = True)