
from flask import Blueprint, render_template, redirect, request
from flask_security import roles_accepted, auth_required
from model import db, Customer, Account, Transaction
from forms import NewCustomerForm, NewAccountForm
from .services import getAccounts, getCustomers, getDate


customerBluePrint = Blueprint('customerpage', __name__)

@customerBluePrint.route('/customer/<id>')
@auth_required()
@roles_accepted("Admin","Staff")
def customerpage(id):
    customer = getCustomers(id)
    summa  =  0
    for accounts in customer.Accounts:
        summa = summa + accounts.Balance
    return render_template("customerpages/customer.html", customer=customer, summa=summa)

@customerBluePrint.route('/customer/account/<id>')
@auth_required()
@roles_accepted("Admin","Staff")
def Transaktioner(id):
    page = int(request.args.get('page', 1))
    account = getAccounts(id)
    transaktioner = Transaction.query.filter_by(AccountId=id)
    transaktioner = transaktioner.order_by(Transaction.Date.desc())
    paginationObject = transaktioner.paginate(page=page, per_page=10, error_out=False)
    return render_template("transactions/transactions.html", account=account, 
                            transaktioner=paginationObject.items,
                            pages=paginationObject.pages,
                            has_next=paginationObject.has_next,
                            has_prev=paginationObject.has_prev,
                            page=page,)

@customerBluePrint.route("/customers")
@auth_required()
@roles_accepted("Admin","Staff")
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
    return render_template("customerpages/customers.html",
                            customers=paginationObject.items,
                            pages=paginationObject.pages,
                            sortOrder=sortOrder,
                            sortColumn=sortColumn,
                            has_next=paginationObject.has_next,
                            has_prev=paginationObject.has_prev,
                            page=page,
                            q=q
                            )

@customerBluePrint.route("/editcustomer/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin")
def editcustomer(id):
    customer = getCustomers(id)
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
        return redirect("/customer/"+ str(customer.Id) )
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
    return render_template("customerpages/editcustomer.html", formen=form )


@customerBluePrint.route("/newcustomer", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin")
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
        newaccount.Created = getDate()
        newaccount.Balance = 0
        customer.Accounts = [newaccount]

        db.session.add(customer)
        db.session.commit()
        return redirect("/customer/"+ str(customer.Id) )
    return render_template("customerpages/newcustomer.html", formen=form )


@customerBluePrint.route("/newaccount/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin","Staff")
def newaccount(id):
    account = getAccounts(id)
    customer = getCustomers(id)
    form = NewAccountForm()
    if form.validate_on_submit():
        newaccount =  Account()
        newaccount.CustomerId = customer.Id
        newaccount.AccountType = form.AccountType.data
        newaccount.Created = getDate()
        newaccount.Balance = 0
        db.session.add(newaccount)
        db.session.commit()
        return redirect("/customer/"+ str(customer.Id) )
    return render_template("customerpages/newaccount.html", formen=form, customer = customer, account = account )