from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, Customer
from random import randint
from forms import NewCustomerForm
import os 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
 

@app.route("/")
def startpage():
    return render_template("index.html")

@app.route("/contact")
def contactpage():
    return render_template("contact.html")

@app.route("/category/<id>")
def category(id):
    return "hej2"
    # products = Product.query.all()
    # return render_template("category.html", products=products)


@app.route("/customer/<id>")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    return render_template("customer.html", customer=customer )

@app.route("/customers")
def customersPage():
    sortColumn = request.args.get('sortColumn', 'name')
    sortOrder = request.args.get('sortOrder', 'asc')
    q = request.args.get('q', '')
    page = int(request.args.get('page', 1))

    customers = Customer.query

    customers = customers.filter(
        Customer.Surname.like('%' + q + '%') |
        Customer.GivenName.like('%' + q + '%') |
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
    # return render_template("customer.html",customers=Customer.query.all())
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
def newcustomer():
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer = Customer()
        customer.Name = form.name.data
        customer.City = form.city.data
        customer.TelephoneCountryCode = 1
        customer.Telephone = "321323"
        db.session.add(customer)
        db.session.commit()
        return redirect("/customers" )
    return render_template("newcustomer.html", formen=form )

@app.route("/editcustomer/<int:id>", methods=['GET', 'POST'])
def editcustomer(id):
    customer = Customer.query.filter_by(Id=id).first()
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer.Name = form.name.data
        customer.City = form.city.data
        db.session.commit()
        return redirect("/customers" )
    if request.method == 'GET':
        form.name .data = customer.Name
        form.city.data = customer.City
    return render_template("editcustomer.html", formen=form )

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
        seedData(db)
        app.run()